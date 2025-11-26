from django.urls import path

from apps.tables.hr_staff_list import hr_staff_list_views as views

urlpatterns = [
    path('hr_staff_list/', views.hr_staff_list, name="hr_staff_list"),
    path('create_hr_staff_list/', views.create_hr_staff_list, name="create_hr_staff_list"),
    path('create-hr-staff-list-filter/', views.create_hr_staff_list_filter, name="create_hr_staff_list_filter"),
    path('create-hr-staff-list-page-items/', views.create_hr_staff_list_page_items, name="create_hr_staff_list_page_items"),
    path('create-hr-staff-list-hide-show-items/', views.create_hr_staff_list_hide_show_filter, name="create_hr_staff_list_hide_show_filter"),
    path('delete-hr-staff-list-filter/<int:id>/', views.delete_hr_staff_list_filter, name="delete_hr_staff_list_filter"),
    path('delete-hr-staff-list-daterange-filter/<int:id>/', views.delete_hr_staff_list_daterange_filter, name="delete_hr_staff_list_daterange_filter"),
    path('delete-hr-staff-list-intrange-filter/<int:id>/', views.delete_hr_staff_list_intrange_filter, name="delete_hr_staff_list_intrange_filter"),
    path('delete-hr-staff-list-floatrange-filter/<int:id>/', views.delete_hr_staff_list_floatrange_filter, name="delete_hr_staff_list_floatrange_filter"),
    path('delete-hr-staff-list/<int:id>/', views.delete_hr_staff_list, name="delete_hr_staff_list"),
    path('update-hr-staff-list/<int:id>/', views.update_hr_staff_list, name="update_hr_staff_list"),

    path('export-hr-staff-list-csv/', views.ExportCSVView.as_view(), name='export_hr_staff_list_csv'),
    path('export-hr-staff-list-excel/', views.ExportExcelView.as_view(), name='export_hr_staff_list_excel'),
    path('export-hr-staff-list-pdf/', views.ExportPDFView.as_view(), name='export_hr_staff_list_pdf'),
]