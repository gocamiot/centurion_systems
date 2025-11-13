import os
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from apps.file_manager.models import File, FileManager
from apps.tables.models import ActionStatus, DocumentStatus, DocumentType
from apps.common.models import Sidebar
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.files.storage import default_storage

# Create your views here.

@login_required
def file_manager(request):
    file_managers = FileManager.objects.filter(parent=None, action_status=ActionStatus.IS_ACTIVE).order_by('-created_at')

    context = {
        'file_managers': file_managers,
        'document_status': DocumentStatus,
        'document_type': DocumentType
    }
    return render(request, 'file_manager/index.html', context)

@login_required
def sub_folders(request, slug):
    parent_folder = get_object_or_404(FileManager, slug=slug)
    root_folder = parent_folder
    while root_folder.parent is not None:
        root_folder = root_folder.parent

    file_managers = FileManager.objects.filter(parent=parent_folder, action_status=ActionStatus.IS_ACTIVE).order_by('-created_at')
    files = File.objects.filter(file_manager=parent_folder, action_status=ActionStatus.IS_ACTIVE).order_by('-uploaded_at')

    context = {
        'file_managers': file_managers,
        'parent_folder': parent_folder,
        'files': files,
        'document_status': DocumentStatus,
        'document_type': DocumentType,
        'segment': root_folder.name,
        'parent': root_folder.sidebar.segment if root_folder.sidebar else ""
    }
    return render(request, 'file_manager/sub_folders.html', context)

@login_required
def create_folder(request, slug=None):
    parent_folder = None
    if slug:
        parent_folder = get_object_or_404(FileManager, slug=slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        file_manager = FileManager.objects.create(
            name=name,
            created_by=request.user,
            updated_by=request.user,
            parent=parent_folder
        )

        group_name = request.POST.get('group_name')
        if sidebar_id := request.POST.get('sidebar'):
            sidebar = get_object_or_404(Sidebar, pk=sidebar_id)
            file_manager.sidebar = sidebar
            file_manager.save()

            group = get_object_or_404(Group, name=group_name)
            dynamic_url = reverse('sub_folders', kwargs={'slug': file_manager.slug})

            Sidebar.objects.create(
                group=group,
                name=name,
                dynamic_url=dynamic_url,
                segment=name,
                parent=sidebar
            )

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def upload_file_to_folder(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        folder_id = request.POST.get('folder_id')
        base_folder = get_object_or_404(FileManager, id=folder_id)

        files = request.FILES.getlist('files')
        paths = request.POST.getlist('paths[]')

        folder_hierarchy = set()
        for relative_path in paths:
            path_obj = Path(relative_path)
            *parts, _ = path_obj.parts
            for i in range(1, len(parts)+1):
                folder_hierarchy.add('/'.join(parts[:i]))

        created_folders = {} 
        for folder_path in sorted(folder_hierarchy):
            parts = folder_path.split('/')
            parent = base_folder
            current_path = ''
            
            for part in parts:
                current_path = f"{current_path}/{part}" if current_path else part
                
                if current_path in created_folders:
                    parent = created_folders[current_path]
                    continue
                
                new_name = part
                counter = 1
                while FileManager.objects.filter(name=new_name, parent=parent, action_status=ActionStatus.IS_ACTIVE).exists():
                    new_name = f"{part}_copy" if counter == 1 else f"{part}_copy{counter}"
                    counter += 1
                
                folder, created = FileManager.objects.get_or_create(
                    name=new_name,
                    parent=parent,
                    action_status=ActionStatus.IS_ACTIVE,
                    defaults={
                        'created_by': request.user,
                        'updated_by': request.user
                    }
                )
                created_folders[current_path] = folder
                parent = folder

        for uploaded_file, relative_path in zip(files, paths):
            path_obj = Path(relative_path)
            *parts, filename = path_obj.parts
            folder_path = '/'.join(parts)
            
            target_folder = created_folders.get(folder_path, base_folder)
            
            File.objects.create(
                file_manager=target_folder,
                file=uploaded_file,
                uploaded_by=request.user,
                updated_by=request.user
            )

        return JsonResponse({'message': f'{len(files)} file(s) uploaded successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def edit_folder(request, pk):
    folder = get_object_or_404(FileManager, pk=pk)
    if request.method == 'POST':
        for attribute, value in request.POST.items():
            if attribute == 'csrfmiddlewaretoken':
                continue

            setattr(folder, attribute, value)
            folder.save()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_folder(request, pk):
    folder = get_object_or_404(FileManager, pk=pk)

    parts = []
    file_manager = folder
    while file_manager:
        parts.insert(0, file_manager.name)
        file_manager = file_manager.parent

    old_path = os.path.join(settings.MEDIA_ROOT, *parts)

    if os.path.exists(old_path) and os.path.isdir(old_path):
        parent_dir = os.path.dirname(old_path)
        new_folder_name = f"del_{folder.name}"
        new_path = os.path.join(parent_dir, new_folder_name)

        try:
            os.rename(old_path, new_path)
            folder.name = new_folder_name
        except Exception as e:
            print(f"Error renaming folder: {e}")

    folder.action_status = ActionStatus.DELETED
    folder.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_file(request, pk):
    file = get_object_or_404(File, pk=pk)

    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        old_name = os.path.basename(file.file.name)

        if new_name and new_name != old_name:
            old_path = file.file.path
            dir_path = os.path.dirname(old_path)
            new_path = os.path.join(dir_path, new_name)

            if not default_storage.exists(new_path):
                with default_storage.open(old_path, 'rb') as f:
                    default_storage.save(new_path, f)
                default_storage.delete(old_path)

                relative_path = os.path.relpath(new_path, settings.MEDIA_ROOT)
                file.file.name = relative_path

        for attribute, value in request.POST.items():
            if attribute in ['csrfmiddlewaretoken', 'name']:
                continue
            setattr(file, attribute, value)

        file.updated_by = request.user
        file.save()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)

    if file.file:
        old_path = file.file.path
        dir_name, file_name = os.path.split(old_path)
        new_file_name = f"del_{file_name}"
        new_path = os.path.join(dir_name, new_file_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            file.file.name = os.path.join(file.file.field.upload_to, new_file_name)

    file.action_status = ActionStatus.DELETED
    file.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@csrf_exempt
def delete_selected_items(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])

            for item in items:
                # Delete FILE
                if item.startswith('file-'):
                    pk = item.replace('file-', '')
                    file = File.objects.filter(pk=pk).first()
                    if file and file.file:
                        old_path = file.file.path
                        dir_name, file_name = os.path.split(old_path)
                        new_file_name = f"del_{file_name}"
                        new_path = os.path.join(dir_name, new_file_name)

                        if os.path.exists(old_path):
                            os.rename(old_path, new_path)
                            relative_path = os.path.relpath(new_path, settings.MEDIA_ROOT)
                            file.file.name = relative_path

                        file.action_status = ActionStatus.DELETED
                        file.save()

                # Delete FOLDER
                elif item.startswith('folder-'):
                    pk = item.replace('folder-', '')
                    folder = FileManager.objects.filter(pk=pk).first()
                    if folder:
                        parts = []
                        file_manager = folder
                        while file_manager:
                            parts.insert(0, file_manager.name)
                            file_manager = file_manager.parent

                        old_path = os.path.join(settings.MEDIA_ROOT, *parts)

                        if os.path.exists(old_path) and os.path.isdir(old_path):
                            parent_dir = os.path.dirname(old_path)
                            new_folder_name = f"del_{folder.name}"
                            new_path = os.path.join(parent_dir, new_folder_name)

                            try:
                                os.rename(old_path, new_path)
                                folder.name = new_folder_name
                            except Exception as e:
                                print(f"Error renaming folder: {e}")

                        folder.action_status = ActionStatus.DELETED
                        folder.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)