from django.urls import path

from apps.tables.analysis_of_security_audits_user_logs import analysis_of_security_audits_user_logs_views as views

urlpatterns = [
    path('analysis_of_security_audits_user_logs/', views.analysis_of_security_audits_user_logs, name="analysis_of_security_audits_user_logs"),
    path('create_analysis_of_security_audits_user_logs/', views.create_analysis_of_security_audits_user_logs, name="create_analysis_of_security_audits_user_logs"),
    path('create-analysis-of-security-audits-user-logs-filter/', views.create_analysis_of_security_audits_user_logs_filter, name="create_analysis_of_security_audits_user_logs_filter"),
    path('create-analysis-of-security-audits-user-logs-page-items/', views.create_analysis_of_security_audits_user_logs_page_items, name="create_analysis_of_security_audits_user_logs_page_items"),
    path('create-analysis-of-security-audits-user-logs-hide-show-items/', views.create_analysis_of_security_audits_user_logs_hide_show_filter, name="create_analysis_of_security_audits_user_logs_hide_show_filter"),
    path('delete-analysis-of-security-audits-user-logs-filter/<int:id>/', views.delete_analysis_of_security_audits_user_logs_filter, name="delete_analysis_of_security_audits_user_logs_filter"),
    path('delete-analysis-of-security-audits-user-logs-daterange-filter/<int:id>/', views.delete_analysis_of_security_audits_user_logs_daterange_filter, name="delete_analysis_of_security_audits_user_logs_daterange_filter"),
    path('delete-analysis-of-security-audits-user-logs-intrange-filter/<int:id>/', views.delete_analysis_of_security_audits_user_logs_intrange_filter, name="delete_analysis_of_security_audits_user_logs_intrange_filter"),
    path('delete-analysis-of-security-audits-user-logs-floatrange-filter/<int:id>/', views.delete_analysis_of_security_audits_user_logs_floatrange_filter, name="delete_analysis_of_security_audits_user_logs_floatrange_filter"),
    path('delete-analysis-of-security-audits-user-logs/<int:id>/', views.delete_analysis_of_security_audits_user_logs, name="delete_analysis_of_security_audits_user_logs"),
    path('update-analysis-of-security-audits-user-logs/<int:id>/', views.update_analysis_of_security_audits_user_logs, name="update_analysis_of_security_audits_user_logs"),

    path('export-analysis-of-security-audits-user-logs-csv/', views.ExportCSVView.as_view(), name='export_analysis_of_security_audits_user_logs_csv'),
    path('export-analysis-of-security-audits-user-logs-excel/', views.ExportExcelView.as_view(), name='export_analysis_of_security_audits_user_logs_excel'),
    path('export-analysis-of-security-audits-user-logs-pdf/', views.ExportPDFView.as_view(), name='export_analysis_of_security_audits_user_logs_pdf'),
]