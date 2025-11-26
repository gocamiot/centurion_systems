from django.urls import path

from apps.tables.privileged_users import privileged_users_views as views

urlpatterns = [
    path('privileged_users/', views.privileged_users, name="privileged_users"),
    path('create_privileged_users/', views.create_privileged_users, name="create_privileged_users"),
    path('create-privileged-users-filter/', views.create_privileged_users_filter, name="create_privileged_users_filter"),
    path('create-privileged-users-page-items/', views.create_privileged_users_page_items, name="create_privileged_users_page_items"),
    path('create-privileged-users-hide-show-items/', views.create_privileged_users_hide_show_filter, name="create_privileged_users_hide_show_filter"),
    path('delete-privileged-users-filter/<int:id>/', views.delete_privileged_users_filter, name="delete_privileged_users_filter"),
    path('delete-privileged-users-daterange-filter/<int:id>/', views.delete_privileged_users_daterange_filter, name="delete_privileged_users_daterange_filter"),
    path('delete-privileged-users-intrange-filter/<int:id>/', views.delete_privileged_users_intrange_filter, name="delete_privileged_users_intrange_filter"),
    path('delete-privileged-users-floatrange-filter/<int:id>/', views.delete_privileged_users_floatrange_filter, name="delete_privileged_users_floatrange_filter"),
    path('delete-privileged-users/<int:id>/', views.delete_privileged_users, name="delete_privileged_users"),
    path('update-privileged-users/<int:id>/', views.update_privileged_users, name="update_privileged_users"),

    path('export-privileged-users-csv/', views.ExportCSVView.as_view(), name='export_privileged_users_csv'),
    path('export-privileged-users-excel/', views.ExportExcelView.as_view(), name='export_privileged_users_excel'),
    path('export-privileged-users-pdf/', views.ExportPDFView.as_view(), name='export_privileged_users_pdf'),
]