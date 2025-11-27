from django.urls import path

from apps.tables.user_logs_vs_privileged_users import user_logs_vs_privileged_users_views as views

urlpatterns = [
    path('user_logs_vs_privileged_users/', views.user_logs_vs_privileged_users, name="user_logs_vs_privileged_users"),
    path('create_user_logs_vs_privileged_users/', views.create_user_logs_vs_privileged_users, name="create_user_logs_vs_privileged_users"),
    path('create-user-logs-vs-privileged-users-filter/', views.create_user_logs_vs_privileged_users_filter, name="create_user_logs_vs_privileged_users_filter"),
    path('create-user-logs-vs-privileged-users-page-items/', views.create_user_logs_vs_privileged_users_page_items, name="create_user_logs_vs_privileged_users_page_items"),
    path('create-user-logs-vs-privileged-users-hide-show-items/', views.create_user_logs_vs_privileged_users_hide_show_filter, name="create_user_logs_vs_privileged_users_hide_show_filter"),
    path('delete-user-logs-vs-privileged-users-filter/<int:id>/', views.delete_user_logs_vs_privileged_users_filter, name="delete_user_logs_vs_privileged_users_filter"),
    path('delete-user-logs-vs-privileged-users-daterange-filter/<int:id>/', views.delete_user_logs_vs_privileged_users_daterange_filter, name="delete_user_logs_vs_privileged_users_daterange_filter"),
    path('delete-user-logs-vs-privileged-users-intrange-filter/<int:id>/', views.delete_user_logs_vs_privileged_users_intrange_filter, name="delete_user_logs_vs_privileged_users_intrange_filter"),
    path('delete-user-logs-vs-privileged-users-floatrange-filter/<int:id>/', views.delete_user_logs_vs_privileged_users_floatrange_filter, name="delete_user_logs_vs_privileged_users_floatrange_filter"),
    path('delete-user-logs-vs-privileged-users/<int:id>/', views.delete_user_logs_vs_privileged_users, name="delete_user_logs_vs_privileged_users"),
    path('update-user-logs-vs-privileged-users/<int:id>/', views.update_user_logs_vs_privileged_users, name="update_user_logs_vs_privileged_users"),

    path('export-user-logs-vs-privileged-users-csv/', views.ExportCSVView.as_view(), name='export_user_logs_vs_privileged_users_csv'),
    path('export-user-logs-vs-privileged-users-excel/', views.ExportExcelView.as_view(), name='export_user_logs_vs_privileged_users_excel'),
    path('export-user-logs-vs-privileged-users-pdf/', views.ExportPDFView.as_view(), name='export_user_logs_vs_privileged_users_pdf'),
]