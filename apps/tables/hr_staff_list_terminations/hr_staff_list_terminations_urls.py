from django.urls import path

from apps.tables.hr_staff_list_terminations import hr_staff_list_terminations_views as views

urlpatterns = [
    path('hr_staff_list_terminations/', views.hr_staff_list_terminations, name="hr_staff_list_terminations"),
    path('create_hr_staff_list_terminations/', views.create_hr_staff_list_terminations, name="create_hr_staff_list_terminations"),
    path('create-hr-staff-list-terminations-filter/', views.create_hr_staff_list_terminations_filter, name="create_hr_staff_list_terminations_filter"),
    path('create-hr-staff-list-terminations-page-items/', views.create_hr_staff_list_terminations_page_items, name="create_hr_staff_list_terminations_page_items"),
    path('create-hr-staff-list-terminations-hide-show-items/', views.create_hr_staff_list_terminations_hide_show_filter, name="create_hr_staff_list_terminations_hide_show_filter"),
    path('delete-hr-staff-list-terminations-filter/<int:id>/', views.delete_hr_staff_list_terminations_filter, name="delete_hr_staff_list_terminations_filter"),
    path('delete-hr-staff-list-terminations-daterange-filter/<int:id>/', views.delete_hr_staff_list_terminations_daterange_filter, name="delete_hr_staff_list_terminations_daterange_filter"),
    path('delete-hr-staff-list-terminations-intrange-filter/<int:id>/', views.delete_hr_staff_list_terminations_intrange_filter, name="delete_hr_staff_list_terminations_intrange_filter"),
    path('delete-hr-staff-list-terminations-floatrange-filter/<int:id>/', views.delete_hr_staff_list_terminations_floatrange_filter, name="delete_hr_staff_list_terminations_floatrange_filter"),
    path('delete-hr-staff-list-terminations/<int:id>/', views.delete_hr_staff_list_terminations, name="delete_hr_staff_list_terminations"),
    path('update-hr-staff-list-terminations/<int:id>/', views.update_hr_staff_list_terminations, name="update_hr_staff_list_terminations"),

    path('export-hr-staff-list-terminations-csv/', views.ExportCSVView.as_view(), name='export_hr_staff_list_terminations_csv'),
    path('export-hr-staff-list-terminations-excel/', views.ExportExcelView.as_view(), name='export_hr_staff_list_terminations_excel'),
    path('export-hr-staff-list-terminations-pdf/', views.ExportPDFView.as_view(), name='export_hr_staff_list_terminations_pdf'),
]