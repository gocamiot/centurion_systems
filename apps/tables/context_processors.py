from apps.tables.models import DocumentStatus, DocumentType, DocumentType_GR
from apps.common.models import Sidebar
from loader.models import DynamicQuery, SAPApi
from django.contrib.auth.models import Group
from home.models import PyFunctionPrompt, PyFunction

def dt_context(request):
    sidebar_dict = {}
    last_prompt = PyFunctionPrompt.objects.last()
    if request.user.is_authenticated:
        user_groups = request.user.groups.all()
        sidebar_items = Sidebar.objects.filter(is_active=True, group__in=user_groups)
        parents = sidebar_items.filter(parent__isnull=True)
        children = sidebar_items.filter(parent__isnull=False)
        
        for parent in parents:
            sidebar_dict[parent] = children.filter(parent=parent)

    return {
        'device_context': 'All Devices',
        'software_context': 'All Software',
        'document_types': DocumentType,
        'Document_Types': DocumentType_GR,
        'document_status': DocumentStatus,
        'sidebar_dict': sidebar_dict,
        'queries': DynamicQuery.objects.all(),
        'sap_apis': SAPApi.objects.all(),
        'sidebars': Sidebar.objects.filter(is_active=True, parent__isnull=True).values('id', 'name'),
        'groups': Group.objects.all(),
        'py_prompt': last_prompt.prompt if last_prompt else None,
        'py_functions': PyFunction.objects.all()
    }