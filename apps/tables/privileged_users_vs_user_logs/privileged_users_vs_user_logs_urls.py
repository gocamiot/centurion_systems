from django.urls import path

from apps.tables.privileged_users_vs_user_logs import privileged_users_vs_user_logs_views as views

urlpatterns = [
    path('privileged_users_vs_user_logs/', views.privileged_users_vs_user_logs, name="privileged_users_vs_user_logs"),
    path('create_privileged_users_vs_user_logs/', views.create_privileged_users_vs_user_logs, name="create_privileged_users_vs_user_logs"),
    path('create-privileged-users-vs-user-logs-filter/', views.create_privileged_users_vs_user_logs_filter, name="create_privileged_users_vs_user_logs_filter"),
    path('create-privileged-users-vs-user-logs-page-items/', views.create_privileged_users_vs_user_logs_page_items, name="create_privileged_users_vs_user_logs_page_items"),
    path('create-privileged-users-vs-user-logs-hide-show-items/', views.create_privileged_users_vs_user_logs_hide_show_filter, name="create_privileged_users_vs_user_logs_hide_show_filter"),
    path('delete-privileged-users-vs-user-logs-filter/<int:id>/', views.delete_privileged_users_vs_user_logs_filter, name="delete_privileged_users_vs_user_logs_filter"),
    path('delete-privileged-users-vs-user-logs-daterange-filter/<int:id>/', views.delete_privileged_users_vs_user_logs_daterange_filter, name="delete_privileged_users_vs_user_logs_daterange_filter"),
    path('delete-privileged-users-vs-user-logs-intrange-filter/<int:id>/', views.delete_privileged_users_vs_user_logs_intrange_filter, name="delete_privileged_users_vs_user_logs_intrange_filter"),
    path('delete-privileged-users-vs-user-logs-floatrange-filter/<int:id>/', views.delete_privileged_users_vs_user_logs_floatrange_filter, name="delete_privileged_users_vs_user_logs_floatrange_filter"),
    path('delete-privileged-users-vs-user-logs/<int:id>/', views.delete_privileged_users_vs_user_logs, name="delete_privileged_users_vs_user_logs"),
    path('update-privileged-users-vs-user-logs/<int:id>/', views.update_privileged_users_vs_user_logs, name="update_privileged_users_vs_user_logs"),

    path('export-privileged-users-vs-user-logs-csv/', views.ExportCSVView.as_view(), name='export_privileged_users_vs_user_logs_csv'),
    path('export-privileged-users-vs-user-logs-excel/', views.ExportExcelView.as_view(), name='export_privileged_users_vs_user_logs_excel'),
    path('export-privileged-users-vs-user-logs-pdf/', views.ExportPDFView.as_view(), name='export_privileged_users_vs_user_logs_pdf'),
]