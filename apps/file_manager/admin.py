from django.contrib import admin
from apps.file_manager.models import File, FileManager

# Register your models here.

@admin.register(FileManager)
class FileManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'action_status', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('action_status', 'created_by')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_manager', 'file', 'file_type', 'file_status', 'uploaded_by', 'uploaded_at')
    search_fields = ('file',)
    list_filter = ('file_status', 'file_type', 'action_status')