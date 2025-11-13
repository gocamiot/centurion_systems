"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from apps.users import views
from django.views.static import serve

admin.site.site_header = "Administration"

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("", include("home.urls")),
    path('admin/password_change/', views.custom_password_change, name='admin_password_change'),
    path('admin/password_change/done/', views.custom_password_change_done, name='password_change_done'),
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("charts/", include("apps.charts.urls")),
    path("tables/", include("apps.tables.urls")),
    path('view-builder/', include('apps.view_builder.urls')),
    path('', include('apps.finding.urls')),
    path('', include('apps.file_manager.urls')),

    path('whap/', include('whap.urls')),
    path('loader/', include('loader.urls')),

    path("tables/", include("apps.tables.tab.tab_urls")),
    path("tables/", include("apps.tables.finding.finding_urls")),
    path("tables/", include("apps.tables.finding_attachment.finding_attachment_urls")),

    path('api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/'      , SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path("__debug__/", include("debug_toolbar.urls")),

    path('sentry-debug/', trigger_error),
    path('i18n/', include('django.conf.urls.i18n')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('tables/', include('apps.tables.image_loader.image_loader_urls')),

    path('tables/', include('apps.tables.images.images_urls')),

    path('tables/', include('apps.tables.unique_details.unique_details_urls')),

    path('tables/', include('apps.tables.ahtuseractivitiesauditresults284.ahtuseractivitiesauditresults284_urls')),

    path('tables/', include('apps.tables.ahtloginaudittrailresults676.ahtloginaudittrailresults676_urls')),

    path('tables/', include('apps.tables.ahtlistofactiveandinactiveusersresults458.ahtlistofactiveandinactiveusersresults458_urls')),

    path('tables/', include('apps.tables.copy_of_sla_hours__may_2025_004.copy_of_sla_hours__may_2025_004_urls')),

    path('tables/', include('apps.tables.hr_data_for_it_general_control_audit.hr_data_for_it_general_control_audit_urls')),

    path('tables/', include('apps.tables.interactivesignins_20250721_20250722.interactivesignins_20250721_20250722_urls')),

    path('tables/', include('apps.tables.aht_hr_list_vs_activeinactive_list.aht_hr_list_vs_activeinactive_list_urls')),

    path('tables/', include('apps.tables.aht_hr_list_vs_activeinactive_list_01.aht_hr_list_vs_activeinactive_list_01_urls')),

    path('tables/', include('apps.tables.aht_hr_list_vs_activeinactive_list_02.aht_hr_list_vs_activeinactive_list_02_urls')),

    path('tables/', include('apps.tables.aht_hr_list_vs_activeinactive_list_03.aht_hr_list_vs_activeinactive_list_03_urls')),

    path('tables/', include('apps.tables.login_audit_trail_results_vs_aht_hr_list.login_audit_trail_results_vs_aht_hr_list_urls')),

    path('tables/', include('apps.tables.aht_user_activities_audit_results_vs_aht_hr_list.aht_user_activities_audit_results_vs_aht_hr_list_urls')),

    path('tables/', include('apps.tables.netsuite_aht_sandboxemployeesearchactiveandinactiveresults.netsuite_aht_sandboxemployeesearchactiveandinactiveresults_urls')),

    path('tables/', include('apps.tables.netsuite_aht_productionemployeesearchactiveandinactive.netsuite_aht_productionemployeesearchactiveandinactive_urls')),

    path('tables/', include('apps.tables.aht_helpdesk_tickets.aht_helpdesk_tickets_urls')),

    path('tables/', include('apps.tables.data_for_it_general_control_audit__terminations_.data_for_it_general_control_audit__terminations__urls')),

    path('tables/', include('apps.tables._terminations_vs_activeinactive._terminations_vs_activeinactive_urls')),

    path('tables/', include('apps.tables._terminations_vs_hr._terminations_vs_hr_urls')),

    path('tables/', include('apps.tables.delta_terminations_vs_hr.delta_terminations_vs_hr_urls')),

    path('tables/', include('apps.tables.delta_hr_vs_netsuite_prod.delta_hr_vs_netsuite_prod_urls')),

    path('tables/', include('apps.tables.delta_terminations_vs_netsuite_prod.delta_terminations_vs_netsuite_prod_urls')),

    path('tables/', include('apps.tables.ads__av.ads__av_urls')),

    path('tables/', include('apps.tables.ads__intune.ads__intune_urls')),

    path('tables/', include('apps.tables.aht__av.aht__av_urls')),

    path('tables/', include('apps.tables.aht__defender.aht__defender_urls')),

    path('tables/', include('apps.tables.asec_devices__defender.asec_devices__defender_urls')),

    path('tables/', include('apps.tables.asec__av.asec__av_urls')),

    path('tables/', include('apps.tables.asec__intune.asec__intune_urls')),

    path('tables/', include('apps.tables.nupay__av.nupay__av_urls')),

    path('tables/', include('apps.tables.nupay__defender.nupay__defender_urls')),

    path('tables/', include('apps.tables.nupay__intune.nupay__intune_urls')),

    path('tables/', include('apps.tables.all_defenderintune_policies.all_defenderintune_policies_urls')),

    path('tables/', include('apps.tables.ahtintune.ahtintune_urls')),

    path('tables/', include('apps.tables.ads__av__status.ads__av__status_urls')),

    path('tables/', include('apps.tables.aht__av__status.aht__av__status_urls')),

    path('tables/', include('apps.tables.asec__av__status.asec__av__status_urls')),

    path('tables/', include('apps.tables.nupay__av__status.nupay__av__status_urls')),

    path('tables/', include('apps.tables.altron_healthtechusers_detailed.altron_healthtechusers_detailed_urls')),

    path('tables/', include('apps.tables.delta_ad_vs_terminations.delta_ad_vs_terminations_urls')),

    path('tables/', include('apps.tables.delta_netsuiteactiveinactive_vs_ad.delta_netsuiteactiveinactive_vs_ad_urls')),

    path('tables/', include('apps.tables.delta__aht_helpdesk_tickets_to_hr.delta__aht_helpdesk_tickets_to_hr_urls')),

    path('tables/', include('apps.tables.altron_healthtechusers_detailed_2.altron_healthtechusers_detailed_2_urls')),

    path('tables/', include('apps.tables.ad_users_1_vs_ad_users_2.ad_users_1_vs_ad_users_2_urls')),

    path('tables/', include('apps.tables.delta_ad2_vs_terminations.delta_ad2_vs_terminations_urls')),

    path('tables/', include('apps.tables.delta_intune_vs_av.delta_intune_vs_av_urls')),

    path('tables/', include('apps.tables.aht_intune_vs_defender.aht_intune_vs_defender_urls')),

    path('tables/', include('apps.tables.delta_aht_intune_vs_defender_2.delta_aht_intune_vs_defender_2_urls')),

    path('tables/', include('apps.tables.delta_defender_vs_intune.delta_defender_vs_intune_urls')),

    path('tables/', include('apps.tables.delta_defender_vs_intune2.delta_defender_vs_intune2_urls')),
    
    path('tables/', include('apps.tables.delta_intune_vs_defender.delta_intune_vs_defender_urls')),

    path('tables/', include('apps.tables.nupay_delta_intune_vs_av.nupay_delta_intune_vs_av_urls')),

    path('tables/', include('apps.tables.nupay_delta_defender_vs_intune.nupay_delta_defender_vs_intune_urls')),
  
    path('tables/', include('apps.tables.fintech_new_employess.fintech_new_employess_urls')),

    path('tables/', include('apps.tables.fintech_terminations.fintech_terminations_urls')),

    path('tables/', include('apps.tables.fintech_master_employee_file.fintech_master_employee_file_urls')),

    path('tables/', include('apps.tables.fintech_consolidated_changes.fintech_consolidated_changes_urls')),

    path('tables/', include('apps.tables.fintech_incidents.fintech_incidents_urls')),

    path('tables/', include('apps.tables.fintech_syspro_operator_list.fintech_syspro_operator_list_urls')),

    path('tables/', include('apps.tables.fintech_syspro_operators_list_.fintech_syspro_operators_list__urls')),

    path('tables/', include('apps.tables.delta_master_employee_vs_terminations.delta_master_employee_vs_terminations_urls')),

    path('tables/', include('apps.tables.fintech_delta_syspro_users_to_terminations.fintech_delta_syspro_users_to_terminations_urls')),

    path('tables/', include('apps.tables.fintech_delta_new_users_to_master_hr.fintech_delta_new_users_to_master_hr_urls')),

    path('tables/', include('apps.tables.fintech_delta_new_users_vs_terminated_users.fintech_delta_new_users_vs_terminated_users_urls')),

    path('tables/', include('apps.tables.fintech_delta_new_users_to_master_hr__using_surname.fintech_delta_new_users_to_master_hr__using_surname_urls')),

    path('tables/', include('apps.tables.fintech_crq_cab_jun24jun25_vitgc.fintech_crq_cab_jun24jun25_vitgc_urls')),

    path('tables/', include('apps.tables.fintech_master_employee_file_adjusted.fintech_master_employee_file_adjusted_urls')),

    path('tables/', include('apps.tables.fintech_aft_crq_closed_with_submit_date_change_request.fintech_aft_crq_closed_with_submit_date_change_request_urls')),

    path('tables/', include('apps.tables.aft_crq_closed_with_submit_datereport_adjusted.aft_crq_closed_with_submit_datereport_adjusted_urls')),

    path('tables/', include('apps.tables.fintech_delta_change_coordinators_vs_hr_list.fintech_delta_change_coordinators_vs_hr_list_urls')),

    path('tables/', include('apps.tables.fintech_delta_change_coordinators_vs_hr_list_2.fintech_delta_change_coordinators_vs_hr_list_2_urls')),

    path('tables/', include('apps.tables.fintech_delta_change_coordinators_vs_terminations.fintech_delta_change_coordinators_vs_terminations_urls')),

    path('tables/', include('apps.tables.user_ad_membership.user_ad_membership_urls')),

    path('tables/', include('apps.tables.ad_users.ad_users_urls')),

    path('tables/', include('apps.tables.ad_devices.ad_devices_urls')),

    path('tables/', include('apps.tables.fintech_delta_terminations_vs_ad.fintech_delta_terminations_vs_ad_urls')),

    path('tables/', include('apps.tables.fintech_delta_syspro_users_vs_ad.fintech_delta_syspro_users_vs_ad_urls')),

    path('tables/', include('apps.tables.ads_software_extract.ads_software_extract_urls')),

    path('tables/', include('apps.tables.ads_delta_intune_vs_software_list.ads_delta_intune_vs_software_list_urls')),

    path('tables/', include('apps.tables.ads_delta_software_list_vs_intune.ads_delta_software_list_vs_intune_urls')),

    path('tables/', include('apps.tables.fintech_delta_hr_list_vs_change_coordinators.fintech_delta_hr_list_vs_change_coordinators_urls')),

    path('tables/', include('apps.tables.fintech_delta_hr_vs_change_controllers_3.fintech_delta_hr_vs_change_controllers_3_urls')),

    path('tables/', include('apps.tables.alpha_list_inc_terminations.alpha_list_inc_terminations_urls')),

    path('tables/', include('apps.tables.hires_wd_jun_24_to_apr_25.hires_wd_jun_24_to_apr_25_urls')),

    path('tables/', include('apps.tables.terms_wd_jun_24_to_apr_25.terms_wd_jun_24_to_apr_25_urls')),
  
    path('tables/', include('apps.tables.ads_delta_hires_vs_alpha_hr_list.ads_delta_hires_vs_alpha_hr_list_urls')),

    path('tables/', include('apps.tables.ads_delta_intune_vs_hr_master.ads_delta_intune_vs_hr_master_urls')),

    path('tables/', include('apps.tables.ads_ad_export_2025.ads_ad_export_2025_urls')),

    path('tables/', include('apps.tables.astea_changes_2024.astea_changes_2024_urls')),

    path('tables/', include('apps.tables.astea_changes_2025.astea_changes_2025_urls')),

    path('tables/', include('apps.tables.employeeslicense_allocations_export_20250905164509.employeeslicense_allocations_export_20250905164509_urls')),

    path('tables/', include('apps.tables.astea_tickets_aug_2024__aug_2025.astea_tickets_aug_2024__aug_2025_urls')),

    path('tables/', include('apps.tables.astea_changes_2025__2024_combined.astea_changes_2025__2024_combined_urls')),

    path('tables/', include('apps.tables.ads_ad_devices.ads_ad_devices_urls')),

    path('tables/', include('apps.tables.ads_user_ad_memberships.ads_user_ad_memberships_urls')),
  
    path('tables/', include('apps.tables.ads_delta_tickets_vs_hr.ads_delta_tickets_vs_hr_urls')),

    path('tables/', include('apps.tables.ads_delta_tickets_vs_hr2.ads_delta_tickets_vs_hr2_urls')),

    path('tables/', include('apps.tables.ads_delta_hr_vs_ad.ads_delta_hr_vs_ad_urls')),

    path('tables/', include('apps.tables.ads_delta_ad_vs_intune.ads_delta_ad_vs_intune_urls')),

    path('tables/', include('apps.tables.ads_delta_licenses_vs_hr.ads_delta_licenses_vs_hr_urls')),

    path('tables/', include('apps.tables.ads_ad_users.ads_ad_users_urls')),

    path('tables/', include('apps.tables.asec_ad.asec_ad_urls')),

    path('tables/', include('apps.tables.asec_delta_ad_vs_intune.asec_delta_ad_vs_intune_urls')),
  
    path('tables/', include('apps.tables.agentscbckcombined.agentscbckcombined_urls')),

    path('tables/', include('apps.tables.fintech__patch_compliance.fintech__patch_compliance_urls')),

    path('tables/', include('apps.tables.fintech__devices_60days.fintech__devices_60days_urls')),

    path('tables/', include('apps.tables.device_control__microsoft_defender.device_control__microsoft_defender_urls')),

    path('tables/', include('apps.tables.sysp_operator_list__adj.sysp_operator_list__adj_urls')),

    path('tables/', include('apps.tables.user_ad_fintech.user_ad_fintech_urls')),

    path('tables/', include('apps.tables.user_ad_memberships_fintec.user_ad_memberships_fintec_urls')),
  
    path('tables/', include('apps.tables.delta_fintech_new_syspro_vs_ad_users.delta_fintech_new_syspro_vs_ad_users_urls')),

    path('tables/', include('apps.tables.ads_delta_ad_vs_hr.ads_delta_ad_vs_hr_urls')),

    path('tables/', include('apps.tables.delta_fintech_new__new_users_syspro_to_hr_master.delta_fintech_new__new_users_syspro_to_hr_master_urls')),
  
    path('tables/', include('apps.tables.fintech_new_entra_report.fintech_new_entra_report_urls')),

    path('tables/', include('apps.tables.fintech_new_staff_listing_.fintech_new_staff_listing__urls')),

    path('tables/', include('apps.tables.fintech_new_syspro_operator_list.fintech_new_syspro_operator_list_urls')),

    path('tables/', include('apps.tables.fintech_new_user_ad.fintech_new_user_ad_urls')),

    path('tables/', include('apps.tables.delta_ads_licenses_vs_ad.delta_ads_licenses_vs_ad_urls')),

    path('tables/', include('apps.tables.ads_defender_agents.ads_defender_agents_urls')),

    path('tables/', include('apps.tables.ads_asec_antivirus.ads_asec_antivirus_urls')),


    path('tables/', include('apps.tables.ads_defender_f.ads_defender_f_urls')),

    path('tables/', include('apps.tables.ads_asec_antivirus_f.ads_asec_antivirus_f_urls')),

    path('tables/', include('apps.tables.astea_license_users.astea_license_users_urls')),
]

urlpatterns += static(settings.MEDIA_URL      , document_root=settings.MEDIA_ROOT     )
