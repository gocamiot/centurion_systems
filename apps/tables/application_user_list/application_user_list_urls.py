from django.urls import path

from apps.tables.application_user_list import application_user_list_views as views

urlpatterns = [
    path('application_user_list/', views.application_user_list, name="application_user_list"),
    path('create_application_user_list/', views.create_application_user_list, name="create_application_user_list"),
    path('create-application-user-list-filter/', views.create_application_user_list_filter, name="create_application_user_list_filter"),
    path('create-application-user-list-page-items/', views.create_application_user_list_page_items, name="create_application_user_list_page_items"),
    path('create-application-user-list-hide-show-items/', views.create_application_user_list_hide_show_filter, name="create_application_user_list_hide_show_filter"),
    path('delete-application-user-list-filter/<int:id>/', views.delete_application_user_list_filter, name="delete_application_user_list_filter"),
    path('delete-application-user-list-daterange-filter/<int:id>/', views.delete_application_user_list_daterange_filter, name="delete_application_user_list_daterange_filter"),
    path('delete-application-user-list-intrange-filter/<int:id>/', views.delete_application_user_list_intrange_filter, name="delete_application_user_list_intrange_filter"),
    path('delete-application-user-list-floatrange-filter/<int:id>/', views.delete_application_user_list_floatrange_filter, name="delete_application_user_list_floatrange_filter"),
    path('delete-application-user-list/<int:id>/', views.delete_application_user_list, name="delete_application_user_list"),
    path('update-application-user-list/<int:id>/', views.update_application_user_list, name="update_application_user_list"),

    path('export-application-user-list-csv/', views.ExportCSVView.as_view(), name='export_application_user_list_csv'),
    path('export-application-user-list-excel/', views.ExportExcelView.as_view(), name='export_application_user_list_excel'),
    path('export-application-user-list-pdf/', views.ExportPDFView.as_view(), name='export_application_user_list_pdf'),
]