import pytesseract
import os, csv
from django.db import models, connections, OperationalError, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection, OperationalError
from django.db import models, connections
from background_task import background
from django.apps import apps
from django.db.utils import IntegrityError
from django.utils import timezone
from django.contrib.admin.models import LogEntry
from django_quill.fields import QuillField
from PIL import Image as PILImage

try:
    from pgvector.django import VectorField
except ImportError:
    pass

User = get_user_model()

# Create your models here.


class ModelChoices(models.TextChoices): 
    ADSDELTA_LICENSED_VS_ANTI_VIRUS_TEST = 'ADSDELTA_LICENSED_VS_ANTI_VIRUS_TEST', 'ADSDELTALicensedVsAntiVirusTest'
    ADSDELTA_LICENSEDVS_ANTI_VIRUS = 'ADSDELTA_LICENSEDVS_ANTI_VIRUS', 'ADSDELTALicensedvsAntiVirus'
    ASTEALICENSEUSERS = 'ASTEALICENSEUSERS', 'Astealicenseusers'
    ADSASEC_ANTIVIRUS_F = 'ADSASEC_ANTIVIRUS_F', 'ADSASECAntivirusF'
    ADS_DEFENDER_F = 'ADS_DEFENDER_F', 'ADSDefenderF'
    ADSASEC_ANTIVIRUS = 'ADSASEC_ANTIVIRUS', 'ADSASECAntivirus'
    ADS_DEFENDER_AGENTS = 'ADS_DEFENDER_AGENTS', 'ADSDefenderAgents'
    DELTAADS_LICENSESVS_AD = 'DELTAADS_LICENSESVS_AD', 'DELTAADSLicensesvsAD'
    FINTECH_NEW_USER_AD = 'FINTECH_NEW_USER_AD', 'FintechNewUserAD'
    FINTECH_NEW_SYSPRO_OPERATOR_LIST = 'FINTECH_NEW_SYSPRO_OPERATOR_LIST', 'FintechNewSysproOperatorList'
    FINTECH_NEW_STAFF_LISTING = 'FINTECH_NEW_STAFF_LISTING', 'FintechNewStaffListing'
    FINTECH_NEW_ENTRA_REPORT = 'FINTECH_NEW_ENTRA_REPORT', 'FintechNewEntraReport'
    DELTA_FINTECH_NEW_NEWUSERS_SYSPROTO_HR_MASTER = 'DELTA_FINTECH_NEW_NEWUSERS_SYSPROTO_HR_MASTER', 'DeltaFintechNewNewusersSysprotoHRMaster'
    ADS_DELTA_A_DVS_HR = 'ADS_DELTA_A_DVS_HR', 'ADSDeltaADvsHR'
    DELTA_FINTECH_NEW_SYSPROVS_A_DUSERS = 'DELTA_FINTECH_NEW_SYSPROVS_A_DUSERS', 'DeltaFintechNewSysprovsADusers'
    USERADMEMBERSHIPS_FINTEC = 'USERADMEMBERSHIPS_FINTEC', 'UseradmembershipsFintec'
    USERAD_FINTECH = 'USERAD_FINTECH', 'UseradFintech'
    SYSP_OPERATOR_LISTADJ = 'SYSP_OPERATOR_LISTADJ', 'SyspOperatorListadj'
    DEVICECONTROL_MICROSOFT_DEFENDER = 'DEVICECONTROL_MICROSOFT_DEFENDER', 'DevicecontrolMicrosoftDefender'
    FINTECH_DEVICES_60 = 'FINTECH_DEVICES_60', 'FintechDevices60days'
    FINTECH_PATCH_COMPLIANCE = 'FINTECH_PATCH_COMPLIANCE', 'FintechPatchCompliance'
    AGENT_SCBCK_COMBINED = 'AGENT_SCBCK_COMBINED', 'AgentSCBCKCombined'
    ASEC_DELTA_A_DVS_INTUNE = 'ASEC_DELTA_A_DVS_INTUNE', 'ASECDeltaADvsIntune'
    ASECAD = 'ASECAD', 'ASECAD'
    ADSAD_USERS = 'ADSAD_USERS', 'ADSADUsers'
    ADS_DELTA_LICENSESVS_HR = 'ADS_DELTA_LICENSESVS_HR', 'ADSDeltaLicensesvsHR'
    ADS_USER_AD_MEMBERSHIPS = 'ADS_USER_AD_MEMBERSHIPS', 'ADSUserADMemberships'
    ADSAD_DEVICES = 'ADSAD_DEVICES', 'ADSADDevices'
    ADS_DELTA_A_DVS_INTUNE = 'ADS_DELTA_A_DVS_INTUNE', 'ADSDeltaADvsIntune'
    ADS_DELTA_H_RVS_AD = 'ADS_DELTA_H_RVS_AD', 'ADSDeltaHRvsAD'
    ADS_DELTA_TICKETSVS_HR_2 = 'ADS_DELTA_TICKETSVS_HR_2', 'ADSDeltaTicketsvsHR2'
    ADS_DELTA_TICKETSVS_HR = 'ADS_DELTA_TICKETSVS_HR', 'ADSDeltaTicketsvsHR'
    ASTEA_CHANGES_20252024 = 'ASTEA_CHANGES_20252024', 'AsteaChanges20252024combined'
    ASTEA_TICKETS_AUG_2024_AUG_2025 = 'ASTEA_TICKETS_AUG_2024_AUG_2025', 'AsteaTicketsAug2024Aug2025'
    EMPLOYEES_LICENSE_ALLOCATIONS_EXPORT_20250905164509 = 'EMPLOYEES_LICENSE_ALLOCATIONS_EXPORT_20250905164509', 'EmployeesLicenseAllocationsExport20250905164509'
    ASTEA_CHANGES_2025 = 'ASTEA_CHANGES_2025', 'AsteaChanges2025'
    ASTEA_CHANGES_2024 = 'ASTEA_CHANGES_2024', 'AsteaChanges2024'
    ADSAD_EXPORT_2025 = 'ADSAD_EXPORT_2025', 'ADSADExport2025'
    ADS_DELTA_INTUNEVS_HR_MASTER = 'ADS_DELTA_INTUNEVS_HR_MASTER', 'ADSDeltaIntunevsHRMaster'
    AD_SDELTA_HIRESVS_ALPHA_H_RLIST = 'AD_SDELTA_HIRESVS_ALPHA_H_RLIST', 'ADSdeltaHiresvsAlphaHRlist'
    TERMS_WD_JUN_24_APR_25 = 'TERMS_WD_JUN_24_APR_25', 'TermsWDJun24toApr25'
    HIRES_WD_JUN_24_APR_25 = 'HIRES_WD_JUN_24_APR_25', 'HiresWDJun24toApr25'
    ALPHALISTINC_TERMINATIONS = 'ALPHALISTINC_TERMINATIONS', 'AlphalistincTerminations'
    FINTECHDELTA_HRVS_CHANGE_CONTROLLERS_3 = 'FINTECHDELTA_HRVS_CHANGE_CONTROLLERS_3', 'FintechdeltaHRVSChangeControllers3'
    FINTECH_DELTA_HR_LISTVS_CHANGE_COORDINATORS = 'FINTECH_DELTA_HR_LISTVS_CHANGE_COORDINATORS', 'FintechDeltaHRListvsChangeCoordinators'
    ADS_DELTA_SOFTWARELISTVS_INTUNE = 'ADS_DELTA_SOFTWARELISTVS_INTUNE', 'ADSDeltaSoftwarelistvsIntune'
    ADS_DELTA_INTUNEVS_SOFTWARELIST = 'ADS_DELTA_INTUNEVS_SOFTWARELIST', 'ADSDeltaIntunevsSoftwarelist'
    ADS_SOFTWARE_EXTRACT = 'ADS_SOFTWARE_EXTRACT', 'ADSSoftwareExtract'
    FINTECH_DELTA_S_YSPROUSERSVS_AD = 'FINTECH_DELTA_S_YSPROUSERSVS_AD', 'FintechDeltaSYsprousersvsAD'
    FINTECH_DELTA_TERMINATIONSVS_AD = 'FINTECH_DELTA_TERMINATIONSVS_AD', 'FintechDeltaTerminationsvsAD'
    AD_DEVICES = 'AD_DEVICES', 'ADDevices'
    AD_USERS = 'AD_USERS', 'ADUsers'
    USER_AD_MEMBERSHIP = 'USER_AD_MEMBERSHIP', 'UserADMembership'
    FINTECH_DELTA_CHANGE_COORDINATORSVS_TERMINATIONS = 'FINTECH_DELTA_CHANGE_COORDINATORSVS_TERMINATIONS', 'FintechDeltaChangeCoordinatorsvsTerminations'
    FINTECH_DELTA_CHANGE_COORDINATORSVS_HR_LIST_2 = 'FINTECH_DELTA_CHANGE_COORDINATORSVS_HR_LIST_2', 'FintechDeltaChangeCoordinatorsvsHRList2'
    FINTECH_DELTA_CHANGE_COORDINATORSVS_HR_LIST = 'FINTECH_DELTA_CHANGE_COORDINATORSVS_HR_LIST', 'FintechDeltaChangeCoordinatorsvsHRList'
    AFTCRQ_CLOSEDWITHSUBMITDATE_REPORTADJUSTED = 'AFTCRQ_CLOSEDWITHSUBMITDATE_REPORTADJUSTED', 'AFTCRQClosedwithsubmitdateReportadjusted'
    FINTECH_AFTCRQ_CLOSEDWITHSUBMITDATE_CHANGE_REQUEST = 'FINTECH_AFTCRQ_CLOSEDWITHSUBMITDATE_CHANGE_REQUEST', 'FintechAFTCRQClosedwithsubmitdateChangeRequest'
    FINTECH_MASTER_EMPLOYEE_FILEADJUSTED = 'FINTECH_MASTER_EMPLOYEE_FILEADJUSTED', 'FintechMasterEmployeeFileadjusted'
    FINTECH_CRQCAB_JUN_24_JUN_25_ITGC = 'FINTECH_CRQCAB_JUN_24_JUN_25_ITGC', 'FintechCRQCABJun24Jun25vITGC'
    FINTECH_DELTA_NEWUSERSTO_MASTER_HR_USINGSURNAME = 'FINTECH_DELTA_NEWUSERSTO_MASTER_HR_USINGSURNAME', 'FintechDeltaNewuserstoMasterHRUsingsurname'
    FINTECH_DELTA_NEWUSERSVS_TERMINATEDUSERS = 'FINTECH_DELTA_NEWUSERSVS_TERMINATEDUSERS', 'FintechDeltaNewusersvsTerminatedusers'
    FINTECH_DELTA_NEWUSERSTO_MASTER_HR = 'FINTECH_DELTA_NEWUSERSTO_MASTER_HR', 'FintechDeltaNewuserstoMasterHR'
    FINTECH_DELTA_SYSPRO_USERSTOTERMINATIONS = 'FINTECH_DELTA_SYSPRO_USERSTOTERMINATIONS', 'FintechDeltaSysproUserstoterminations'
    DELTA_MASTER_EMPLOYEEVS_TERMINATIONS = 'DELTA_MASTER_EMPLOYEEVS_TERMINATIONS', 'DeltaMasterEmployeevsTerminations'
    FINTECH_SYSPRO_OPERATORS_LIST = 'FINTECH_SYSPRO_OPERATORS_LIST', 'FintechSysproOperatorsList'
    FINTECH_SYSPRO_OPERATOR_LIST = 'FINTECH_SYSPRO_OPERATOR_LIST', 'FintechSysproOperatorList'
    FINTECH_INCIDENTS = 'FINTECH_INCIDENTS', 'FintechIncidents'
    FINTECH_CONSOLIDATED_CHANGES = 'FINTECH_CONSOLIDATED_CHANGES', 'FintechConsolidatedChanges'
    FINTECH_MASTER_EMPLOYEE_FILE = 'FINTECH_MASTER_EMPLOYEE_FILE', 'FintechMasterEmployeeFile'
    FINTECH_TERMINATIONS = 'FINTECH_TERMINATIONS', 'FintechTerminations'
    FINTECH_NEW_EMPLOYESS = 'FINTECH_NEW_EMPLOYESS', 'FintechNewEmployess'
    NU_PAY_DELTA_DEFENDERVS_INTUNE = 'NU_PAY_DELTA_DEFENDERVS_INTUNE', 'NuPayDeltaDefendervsIntune'
    NUPAY_DELTA_INTUNEVS_AV = 'NUPAY_DELTA_INTUNEVS_AV', 'NupayDeltaIntunevsAV'
    DELTA_INTUNEVS_DEFENDER = 'DELTA_INTUNEVS_DEFENDER', 'DeltaIntunevsDefender'
    DELTA_DEFENDERVS_INTUNE_2 = 'DELTA_DEFENDERVS_INTUNE_2', 'DeltaDefendervsIntune2'
    DELTA_DEFENDERVS_INTUNE = 'DELTA_DEFENDERVS_INTUNE', 'DeltaDefendervsIntune'
    DELTA_AHT_INTUNEVS_DEFENDER_2 = 'DELTA_AHT_INTUNEVS_DEFENDER_2', 'DeltaAHTIntunevsDefender2'
    AHT_INTUNEVS_DEFENDER = 'AHT_INTUNEVS_DEFENDER', 'AHTIntunevsDefender'
    DELTA_INTUNEVS_AV = 'DELTA_INTUNEVS_AV', 'DeltaIntunevsAV'
    DELTA_AD_2_TERMINATIONS = 'DELTA_AD_2_TERMINATIONS', 'DeltaAD2vsTerminations'
    AD_USERS_1_VS_AD_USERS_2 = 'AD_USERS_1_VS_AD_USERS_2', 'ADUsers1VsADUsers2'
    ALTRON_HEALTH_TECH_USERS_DETAILED_2 = 'ALTRON_HEALTH_TECH_USERS_DETAILED_2', 'AltronHealthTechUsersDetailed2'
    DELTA_AHT_HELPDESKTICKETSTO_HR = 'DELTA_AHT_HELPDESKTICKETSTO_HR', 'DeltaAHTHelpdeskticketstoHR'
    DELTA_NETSUITE_ACTIVE_INACTIVEVS_AD = 'DELTA_NETSUITE_ACTIVE_INACTIVEVS_AD', 'DeltaNetsuiteActiveInactivevsAD'
    DELTA_A_DVS_TERMINATIONS = 'DELTA_A_DVS_TERMINATIONS', 'DeltaADvsTerminations'
    ALTRON_HEALTH_TECH_USERS_DETAILED = 'ALTRON_HEALTH_TECH_USERS_DETAILED', 'AltronHealthTechUsersDetailed'
    NUPAY_AV_STATUS = 'NUPAY_AV_STATUS', 'NupayAVStatus'
    ASECAV_STATUS = 'ASECAV_STATUS', 'ASECAVStatus'
    AHTAV_STATUS = 'AHTAV_STATUS', 'AHTAVStatus'
    ADSAV_STATUS = 'ADSAV_STATUS', 'ADSAVStatus'
    AHT_INTUNE = 'AHT_INTUNE', 'AHTIntune'
    ALL_DEFENDER_INTUNE_POLICIES = 'ALL_DEFENDER_INTUNE_POLICIES', 'AllDefenderIntunePolicies'
    NUPAY_INTUNE = 'NUPAY_INTUNE', 'NupayIntune'
    NUPAY_DEFENDER = 'NUPAY_DEFENDER', 'NupayDefender'
    NUPAY_AV = 'NUPAY_AV', 'NupayAV'
    ASEC_INTUNE = 'ASEC_INTUNE', 'ASECIntune'
    ASECAV = 'ASECAV', 'ASECAV'
    ASEC_DEVICES_DEFENDER = 'ASEC_DEVICES_DEFENDER', 'ASECDevicesDefender'
    AHT_DEFENDER = 'AHT_DEFENDER', 'AHTDefender'
    AHTAV = 'AHTAV', 'AHTAV'
    ADS_INTUNE = 'ADS_INTUNE', 'ADSIntune'
    ADSAV = 'ADSAV', 'ADSAV'
    DELTA_TERMINATIONS_VS_NETSUITE_PROD = 'DELTA_TERMINATIONS_VS_NETSUITE_PROD', 'DeltaTerminationsVSNetsuiteProd'
    DELTA_HRVS_NETSUITE_PROD = 'DELTA_HRVS_NETSUITE_PROD', 'DeltaHRVSNetsuiteProd'
    DELTA_TERMINATIONS_VSHR = 'DELTA_TERMINATIONS_VSHR', 'DeltaTerminationsVSHR'
    TERMINATIONS_VSHR = 'TERMINATIONS_VSHR', 'TerminationsVSHR'
    TERMINATIONS_VS_ACTIVE_INACTIVE = 'TERMINATIONS_VS_ACTIVE_INACTIVE', 'TerminationsVSActiveInactive'
    DATAFOR_IT_GENERAL_CONTROL_AUDIT_TERMINATIONS = 'DATAFOR_IT_GENERAL_CONTROL_AUDIT_TERMINATIONS', 'DataforITGeneralControlAuditTerminations'
    AHT_HELPDESK_TICKETS = 'AHT_HELPDESK_TICKETS', 'AHTHelpdeskTickets'
    NETSUITE_AHT_PRODUCTION_EMPLOYEE_SEARCH_ACTIVEAND_INACTIVE = 'NETSUITE_AHT_PRODUCTION_EMPLOYEE_SEARCH_ACTIVEAND_INACTIVE', 'NetsuiteAHTProductionEmployeeSearchActiveandInactive'
    NETSUITE_AHT_SANDBOX_EMPLOYEE_SEARCH_ACTIVEAND_INACTIVE_RESULTS = 'NETSUITE_AHT_SANDBOX_EMPLOYEE_SEARCH_ACTIVEAND_INACTIVE_RESULTS', 'NetsuiteAHTSandboxEmployeeSearchActiveandInactiveResults'
    AHT_USER_ACTIVITIES_AUDIT_RESULTS_VSAHTHR_LIST = 'AHT_USER_ACTIVITIES_AUDIT_RESULTS_VSAHTHR_LIST', 'AHTUserActivitiesAuditResultsVSAHTHRList'
    LOGIN_AUDIT_TRAIL_RESULTS_VSAHTHR_LIST = 'LOGIN_AUDIT_TRAIL_RESULTS_VSAHTHR_LIST', 'LoginAuditTrailResultsVSAHTHRList'
    AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST_03 = 'AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST_03', 'AHTHRListVsActiveInactiveList03'
    AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST_02 = 'AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST_02', 'AHTHRListVsActiveInactiveList02'
    AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST_01 = 'AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST_01', 'AHTHRListVsActiveInactiveList01'
    AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST = 'AHTHR_LIST_VS_ACTIVE_INACTIVE_LIST', 'AHTHRListVsActiveInactiveList'
    INTERACTIVE_SIGN_INS_2025072120250722 = 'INTERACTIVE_SIGN_INS_2025072120250722', 'InteractiveSignIns2025072120250722'
    HR_DATAFOR_IT_GENERAL_CONTROL_AUDIT = 'HR_DATAFOR_IT_GENERAL_CONTROL_AUDIT', 'HRDataforITGeneralControlAudit'
    COPYOF_SL_AHOURS_MAY_2025004 = 'COPYOF_SL_AHOURS_MAY_2025004', 'CopyofSLAhoursMay2025004'
    AHT_LISTOF_ACTIVEAND_INACTIVE_USERS_RESULTS_458 = 'AHT_LISTOF_ACTIVEAND_INACTIVE_USERS_RESULTS_458', 'AHTListofActiveandInactiveUsersResults458'
    AHT_LOGIN_AUDIT_TRAIL_RESULTS_676 = 'AHT_LOGIN_AUDIT_TRAIL_RESULTS_676', 'AHTLoginAuditTrailResults676'
    AHT_USER_ACTIVITIES_AUDIT_RESULTS_284 = 'AHT_USER_ACTIVITIES_AUDIT_RESULTS_284', 'AHTUserActivitiesAuditResults284'
    EMPLOYEE_LISTING_APR_25 = 'EMPLOYEE_LISTING_APR_25', 'EmployeeListingApr25'
    SCHEMA_AUDIT_DATABASE_USERS = 'SCHEMA_AUDIT_DATABASE_USERS', 'SchemaAuditDatabaseUsers'
    FAVORITE = 'FAVORITE', _('Favorite')
    UNIQUE = 'UNIQUE', _('Unique')
    FINDING = 'FINDING', _('Finding')
    TAB = 'TAB', _('Tab')
    COPY_DT = 'COPY_DT', _('Copy DT')
    FINDING_VIEW = 'FINDING_VIEW', _('Finding View')
    IMAGE_LOADER = 'IMAGE_LOADER', _('Image Loader')
    IMAGES = 'IMAGES', 'Images'
    FINDING_ATTACHMENT = 'FINDING_ATTACHMENT', 'Finding Attachment'


class Common(models.Model):
    parent = models.CharField(max_length=255, choices=ModelChoices.choices)
    value = models.CharField(max_length=255)

    class Meta:
        abstract = True


class PageItems(models.Model):
    userID = models.IntegerField()
    parent = models.CharField(max_length=255, choices=ModelChoices.choices)
    items_per_page = models.IntegerField(default=25)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)
    

class HideShowFilter(Common):
    userID = models.IntegerField()
    parent = models.CharField(max_length=255, choices=ModelChoices.choices)
    key = models.CharField(max_length=255)
    value = models.BooleanField(default=False)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.key

class ServerFilter(Common):
    userID = models.IntegerField()
    key = models.CharField(max_length=255)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.key


class UserFilter(Common):
    userID = models.IntegerField()
    parent = models.CharField(max_length=255, choices=ModelChoices.choices, null=True, blank=True)
    key = models.CharField(max_length=255)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.key
    

class DateRangeFilter(models.Model):
    userID = models.IntegerField()
    parent = models.CharField(max_length=255, choices=ModelChoices.choices)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    key = models.CharField(max_length=255)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.key

class IntRangeFilter(models.Model):
    userID = models.IntegerField()
    parent = models.CharField(max_length=255, choices=ModelChoices.choices)
    from_number = models.IntegerField(null=True, blank=True)
    to_number = models.IntegerField(null=True, blank=True)
    key = models.CharField(max_length=255)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.key


class FloatRangeFilter(models.Model):
    userID = models.IntegerField()
    parent = models.CharField(max_length=255, choices=ModelChoices.choices)
    from_float_number = models.FloatField(null=True, blank=True)
    to_float_number = models.FloatField(null=True, blank=True)
    key = models.CharField(max_length=255)
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.key


class ActionStatus(models.TextChoices):
    IS_ACTIVE = 'IS_ACTIVE', _('Is Active')
    DELETED = 'DELETED', _('Deleted')

class VendorLinked(models.Model):
    base_string = models.TextField()
    match_string = models.TextField()


class ApplicationLinked(models.Model):
    base_string = models.TextField()
    match_string = models.TextField()

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import uuid

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'app_label__in': getattr(settings, 'LOADER_MODEL_APPS')},
        verbose_name = 'DT'
    )
    model_choices = models.CharField(max_length=255)
    pre_filters = models.TextField(null=True, blank=True)
    pre_columns = models.TextField(null=True, blank=True)
    richtext_fields = models.TextField(null=True, blank=True)
    page_items = models.ForeignKey(PageItems, on_delete=models.SET_NULL, null=True, blank=True)
    hide_show_filters = models.ManyToManyField(HideShowFilter, blank=True)
    user_filters = models.ManyToManyField(UserFilter, blank=True)
    server_filters = models.ManyToManyField(ServerFilter, blank=True)
    date_range_filters = models.ManyToManyField(DateRangeFilter, blank=True)
    int_range_filters = models.ManyToManyField(IntRangeFilter, blank=True)
    float_range_filters = models.ManyToManyField(FloatRangeFilter, blank=True)
    saved_filters = models.ManyToManyField('common.SavedFilter', blank=True)
    # search_items = models.JSONField(null=True, blank=True)
    search = models.CharField(max_length=255, null=True, blank=True)
    order_by = models.CharField(max_length=255, null=True, blank=True)
    snapshot = models.CharField(max_length=255, null=True, blank=True)
    query_snapshot = models.CharField(max_length=255, null=True, blank=True)
    is_dynamic_query = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    has_documents = models.BooleanField(default=False)
    is_split_dt = models.BooleanField(default=False)
    parent_dt = models.UUIDField(null=True, blank=True)
    match_field = models.CharField(max_length=255, null=True, blank=True)
    child_dt = models.UUIDField(null=True, blank=True)
    img_loader_id = models.UUIDField(null=True, blank=True)

    action_status = models.CharField(max_length=50, choices=ActionStatus.choices, default=ActionStatus.IS_ACTIVE)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


class Tab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'app_label__in': getattr(settings, 'LOADER_MODEL_APPS')},
        verbose_name = 'DT'
    )
    model_choices = models.CharField(max_length=255)
    pre_filters = models.TextField(null=True, blank=True)
    pre_columns = models.TextField(null=True, blank=True)
    richtext_fields = models.TextField(null=True, blank=True)
    page_items = models.ForeignKey(PageItems, on_delete=models.SET_NULL, null=True, blank=True)
    hide_show_filters = models.ManyToManyField(HideShowFilter, blank=True)
    user_filters = models.ManyToManyField(UserFilter, blank=True)
    server_filters = models.ManyToManyField(ServerFilter, blank=True)
    date_range_filters = models.ManyToManyField(DateRangeFilter, blank=True)
    int_range_filters = models.ManyToManyField(IntRangeFilter, blank=True)
    float_range_filters = models.ManyToManyField(FloatRangeFilter, blank=True)
    saved_filters = models.ManyToManyField('common.SavedFilter', blank=True)
    # search_items = models.JSONField(null=True, blank=True)
    search = models.CharField(max_length=255, null=True, blank=True)
    order_by = models.CharField(max_length=255, null=True, blank=True)
    snapshot = models.CharField(max_length=255, null=True, blank=True)
    query_snapshot = models.CharField(max_length=255, null=True, blank=True)
    is_dynamic_query = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    has_documents = models.BooleanField(default=False)
    is_split_dt = models.BooleanField(default=False)
    parent_dt = models.UUIDField(null=True, blank=True)
    match_field = models.CharField(max_length=255, null=True, blank=True)
    child_dt = models.UUIDField(null=True, blank=True)
    img_loader_id = models.UUIDField(null=True, blank=True)
    base_view = models.TextField(null=True, blank=True)
    sidebar_parent = models.TextField(null=True, blank=True)
    selected_rows = models.TextField(null=True, blank=True)

    action_status = models.CharField(max_length=50, choices=ActionStatus.choices, default=ActionStatus.IS_ACTIVE)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

class TabNotes(models.Model):
    tab = models.OneToOneField(Tab, on_delete=models.CASCADE)
    note = QuillField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

class EmailActionStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLOSE = 'CLOSE', 'Close'

class Finding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = QuillField(null=True, blank=True)
    recommendation = QuillField(null=True, blank=True)
    #status = models.TextField(null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'app_label__in': getattr(settings, 'LOADER_MODEL_APPS')},
        verbose_name = 'DT',
        null=True, blank=True
    )
    model_choices = models.CharField(max_length=255)
    pre_filters = models.TextField(null=True, blank=True)
    pre_columns = models.TextField(null=True, blank=True)
    richtext_fields = models.TextField(null=True, blank=True)
    page_items = models.ForeignKey(PageItems, on_delete=models.SET_NULL, null=True, blank=True)
    hide_show_filters = models.ManyToManyField(HideShowFilter, blank=True)
    user_filters = models.ManyToManyField(UserFilter, blank=True)
    server_filters = models.ManyToManyField(ServerFilter, blank=True)
    date_range_filters = models.ManyToManyField(DateRangeFilter, blank=True)
    int_range_filters = models.ManyToManyField(IntRangeFilter, blank=True)
    float_range_filters = models.ManyToManyField(FloatRangeFilter, blank=True)
    saved_filters = models.ManyToManyField('common.SavedFilter', blank=True)
    # search_items = models.JSONField(null=True, blank=True)
    search = models.CharField(max_length=255, null=True, blank=True)
    order_by = models.CharField(max_length=255, null=True, blank=True)
    snapshot = models.CharField(max_length=255, null=True, blank=True)
    query_snapshot = models.CharField(max_length=255, null=True, blank=True)
    is_dynamic_query = models.BooleanField(default=False)
    has_documents = models.BooleanField(default=False)
    is_split_dt = models.BooleanField(default=False)
    parent_dt = models.UUIDField(null=True, blank=True)
    match_field = models.CharField(max_length=255, null=True, blank=True)
    child_dt = models.UUIDField(null=True, blank=True)
    selected_rows = models.TextField(null=True, blank=True)

    # Action   
    companies = models.CharField(max_length=255, null=True, blank=True)
    itgc_categories = models.CharField(max_length=255, null=True, blank=True)
    itgc_questions = models.CharField(max_length=255, null=True, blank=True)
    action_type = models.CharField(max_length=255, null=True, blank=True)
    # action_to = models.CharField(max_length=255, null=True, blank=True)
    action_deadline = models.DateTimeField(null=True, blank=True)
    action_note = models.TextField(null=True, blank=True)
    email_action_status = models.CharField(
        max_length=20, 
        choices=EmailActionStatus.choices, 
        default=EmailActionStatus.OPEN
    )

    action_status = models.CharField(max_length=50, choices=ActionStatus.choices, default=ActionStatus.IS_ACTIVE)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=255, null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    version_control = models.IntegerField(default=1, editable=False)

    date_fields_to_convert = []
    integer_fields = []                                                                                                                                                                                          
    float_fields = []

    @property
    def is_parent(self):
        return self.finding_set.exists()

class DocumentStatus(models.TextChoices):
    APPROVED = 'Approved', 'Approved'
    NOTAPPROVED = 'Not Approved', 'Not Approved'

class AttachmentType(models.TextChoices):
    EVIDENCE = 'EVIDENCE', 'Evidence'
    INSIGHTS = 'INSIGHTS', 'Insights'

class FindingAttachment(models.Model):
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='attachment')
    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
    description = models.TextField(null=True, blank=True)
    attachment_status = models.CharField(max_length=50, choices=DocumentStatus.choices)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    version = models.TextField(null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    version_control = models.IntegerField(default=1, editable=False)

    action_status = models.CharField(max_length=50, choices=ActionStatus.choices, default=ActionStatus.IS_ACTIVE)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=255, null=True, blank=True)

    file_fields = ['attachment']
    date_fields_to_convert = []
    integer_fields = []                                                                                                                                                                                          
    float_fields = []

    @property
    def is_parent(self):
        return self.findingattachment_set.exists()

    @property
    def csv_text(self):
        if self.attachment and self.attachment.name.endswith('.csv'):
            try:
                file_path = self.attachment.path
                if not os.path.exists(file_path):
                    return "File does not exist."

                with open(file_path, 'r', encoding='latin-1') as file:
                    reader = csv.reader(file)
                    rows = list(reader)

                text = '\n'.join([','.join(row) for row in rows])
                return text

            except Exception as e:
                return f"Error reading CSV file: {str(e)}"

        return "No CSV file available."

class FindingAction(models.Model):
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name="actions")
    action_to = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=EmailActionStatus.choices,
        default=EmailActionStatus.OPEN,
        verbose_name='Action Status'
    )

    class Meta:
        unique_together = ('finding', 'action_to')

class TableDropdownItem(models.Model):
    item = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    loader_instance = models.IntegerField(null=True, blank=True)


class TableDropdownSubItem(models.Model):
    item = models.ForeignKey(TableDropdownItem, on_delete=models.CASCADE, related_name="subitems")
    subitem = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

class DependentDropdown(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)



class DocumentType(models.TextChoices):
    CONTRACT = 'Contract', 'Contract'
    INVOICE = 'Invoice', 'Invoice'
    STATEMENT = 'Statement', 'Statement'
  
class DocumentType_GR(models.TextChoices):
    Design  = 'Design', 'Design'
    Framework  = 'Framework', 'Framework'
    Guideline  = 'Guideline', 'Guideline'
    Noting  = 'Noting', 'Noting'
    Policy  = 'Policy', 'Policy'
    Procedure  = 'Procedure', 'Procedure'
    Process  = 'Process', 'Process'
    Standard  = 'Standard', 'Standard'
    No_Longer_Required  = 'No Longer Required', 'No_Longer_Required'
    Red_Line_Draft  = 'Red Line Draft', 'Red_Line_Draft'

BATCH_SIZE = 5000

def database_connection(db, query="SELECT 1"):
    try:
        connection_params = {
            'ENGINE': db.db_type if db.db_type == 'mssql' else f'django.db.backends.{db.db_type}',
            'NAME': db.db_name,
            'USER': db.db_user,
            'PASSWORD': db.db_pass,
            'HOST': db.db_host if db.db_type != 'mssql' else f"{db.db_host},{db.db_port}",
            'PORT': db.db_port if db.db_type != 'mssql' else '',
            'ATOMIC_REQUESTS': False,
            'TIME_ZONE': 'UTC',
            'CONN_HEALTH_CHECKS': False,
            'CONN_MAX_AGE': 0,
            'AUTOCOMMIT': True,
            'OPTIONS': {
                'connect_timeout': 5,
            }
        }
        if db.db_type == DBType.mssql:
            connection_params['OPTIONS']["driver"] = "ODBC Driver 17 for SQL Server"

        connections.databases[db.db_name] = connection_params
        result = ""
        row_count = 0
        columns = []
        with connections[db.db_name].cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            row_count = cursor.rowcount
            columns = [col[0] for col in cursor.description]

        db.connected = True

        try:
            call_command('makemigrations', interactive=False, verbosity=0)
            call_command('migrate', database=db.db_name, interactive=False, verbosity=0)
            print(f"Migrated successfully!")
        except Exception as e:
            print(f"Migration failed: {e}")

        return result, row_count, columns

    except OperationalError:
        db.connected = False


def mssql_database_connection(db, query="SELECT 1"):
    try:
        connection_params = {
            'ENGINE': db.db_type,
            'NAME': db.db_name,
            'USER': db.db_user,
            'PASSWORD': db.db_pass,
            'HOST': f"{db.db_host},{db.db_port}",
            'ATOMIC_REQUESTS': False,
            'TIME_ZONE': 'UTC',
            'CONN_HEALTH_CHECKS': False,
            'CONN_MAX_AGE': 0,
            'AUTOCOMMIT': True,
            'OPTIONS': {
                'connect_timeout': 5,
                "driver": "ODBC Driver 17 for SQL Server",
            }
        }

        connections.databases[db.db_name] = connection_params
        result = ""
        row_count = 0
        with connections[db.db_name].cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            row_count = cursor.rowcount

        db.connected = True

        return result, row_count

    except OperationalError:
        db.connected = False


class DBType(models.TextChoices):
    postgresql = 'postgresql', 'PostgreSQL'
    mysql = 'mysql', 'MySQL'
    mssql = 'mssql', 'SQL Server'


class ExternalDatabase(models.Model):
    db_type = models.CharField(max_length=100, choices=DBType.choices)
    connection_name = models.CharField(max_length=255, unique=True)
    db_name = models.CharField(max_length=255)
    db_user = models.CharField(max_length=255)
    db_pass = models.CharField(max_length=255)
    db_host = models.CharField(max_length=255)
    db_port = models.CharField(max_length=255)
    connected = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.connection_name


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.db_type == DBType.mssql:
            mssql_database_connection(self)
        else:
            database_connection(self)

        if self._state.adding:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        super().save(*args, **kwargs)


class TemporaryTable(models.Model):
    database = models.ForeignKey(
        ExternalDatabase, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="For local database like sqlite keep this field empty"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name = 'Choose model',
        related_name='temporary_table'
    )
    temporary_table_name = models.CharField(max_length=255, unique=True)
    query = models.TextField()
    is_correct = models.BooleanField(default=False, editable=False)
    rows = models.IntegerField(null=True, blank=True)
    error_log = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.temporary_table_name

    def save(self, *args, **kwargs):
        try:
            if self.database:
                if self.database.db_type == DBType.mssql:
                    result, row_count = mssql_database_connection(self.database, self.query)
                    if result and row_count:
                        self.rows = row_count
                        self.is_correct = True

                else:
                    result, row_count = database_connection(self.database, self.query)
                    if result and row_count:
                        self.rows = row_count
                        self.is_correct = True
            else:
                with connection.cursor() as cursor:
                    cursor.execute(self.query)
                    self.is_correct = True
                    self.rows = cursor.rowcount
            
        except OperationalError as e:
            self.is_correct = False
            self.error_log = str(e)

        if self._state.adding:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        super().save(*args, **kwargs)


class DynamicQuery(models.Model):
    database = models.ForeignKey(
        ExternalDatabase, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="For local database like sqlite keep this field empty"
    )
    view_name = models.CharField(max_length=255, unique=True)
    query = models.TextField()
    temporary_tables = models.ManyToManyField(TemporaryTable, blank=True)
    is_correct = models.BooleanField(default=False, editable=False)
    rows = models.IntegerField(null=True, blank=True)
    error_log = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.view_name

    def save(self, *args, **kwargs):
        try:
            if self.database:
                if self.database.db_type == DBType.mssql:
                    result, row_count = mssql_database_connection(self.database, self.query)
                    if result and row_count:
                        self.rows = row_count
                        self.is_correct = True

                else:
                    result, row_count = database_connection(self.database, self.query)
                    if result and row_count:
                        self.rows = row_count
                        self.is_correct = True
            else:
                with connection.cursor() as cursor:
                    cursor.execute(self.query)
                    self.is_correct = True
                    self.rows = cursor.rowcount
            
        except OperationalError as e:
            self.is_correct = False
            self.error_log = str(e)

        if self._state.adding:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        super().save(*args, **kwargs)

class TaskStatus(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class ExportDB(models.Model):
    export_to = models.ForeignKey(ExternalDatabase, on_delete=models.CASCADE, related_name="export_db")
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Export Database'
        verbose_name_plural = 'Export Databases'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self._state.adding:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        export_data_to_external_db(self.pk)


class ExportLog(models.Model):
    model_name = models.CharField(max_length=255)
    count_b_copy = models.CharField(max_length=50, null=True, blank=True, verbose_name="Count before copy")
    count_a_copy = models.CharField(max_length=50, null=True, blank=True, verbose_name="Count after copy")
    success = models.BooleanField(default=False)
    error_log = models.TextField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.model_name

@background(schedule=0)
def export_data_to_external_db(pk):
    print("Starting to copy data...")
    export_to = ExportDB.objects.get(pk=pk)
    db = export_to.export_to
    all_models = apps.get_models()
    excluded_models = [ExportDB, LogEntry]

    def get_batch(queryset, start, end):
        return list(queryset[start:end])

    def copy_model_data(model):
        if model._meta.managed and model not in excluded_models:
            database_connection(db)
            try:
                source_count = model.objects.using('default').count()
                export_log = ExportLog.objects.create(
                    model_name=model._meta.model_name,
                    count_b_copy=source_count,
                    start_at=timezone.now()
                )
                SUCCESS = True
                for start in range(0, source_count, BATCH_SIZE):
                    end = min(start + BATCH_SIZE, source_count)
                    batch = get_batch(model.objects.using('default').all(), start, end)
                    for instance in batch:
                        try:
                            # Check if a record with the same primary key already exists
                            if model.objects.using(db.db_name).filter(pk=instance.pk).exists():
                                continue

                            # Check for unique constraints
                            unique_fields = [field for field in model._meta.fields if field.unique]
                            duplicate_found = False
                            for field in unique_fields:
                                field_value = getattr(instance, field.name)
                                if model.objects.using(db.db_name).filter(**{field.name: field_value}).exists():
                                    duplicate_found = True
                                    break

                            if duplicate_found:
                                continue

                            # Save related objects if necessary
                            for related_field in instance._meta.get_fields():
                                if related_field.is_relation and related_field.many_to_one:
                                    related_object = getattr(instance, related_field.name)
                                    if related_object:
                                        related_model = related_field.related_model
                                        if not related_model.objects.using(db.db_name).filter(pk=related_object.pk).exists():
                                            related_object.save(using=db.db_name)

                            instance.save(using=db.db_name)
                            export_log.count_a_copy = model.objects.using(db.db_name).count()
                            export_log.success = True
                            export_log.finished_at = timezone.now()
                            export_log.save()

                        except IntegrityError as e:
                            SUCCESS = False
                            print(f"IntegrityError copying data for model {model._meta.model_name} and instance {instance.pk}: {e}")
                            # export_log.error_log = f"IntegrityError copying data for model {model._meta.model_name} and instance {instance.pk}: {e}\n"
                        except Exception as e:
                            SUCCESS = False
                            print(f"Error copying data for model {model._meta.model_name} and instance {instance.pk}: {e}")
                            # export_log.error_log = f"Error copying data for model {model._meta.model_name} and instance {instance.pk}: {e}\n"

                    print(f"Copied batch of {len(batch)} rows for model {model._meta.model_name}")

                export_log.count_a_copy = model.objects.using(db.db_name).count()
                export_log.success = SUCCESS
                export_log.finished_at = timezone.now()
                export_log.save()

                print(f"Copied {export_log.count_a_copy} rows for model {model._meta.model_name}")

            except Exception as e:
                print(f"Error copying data for model {model._meta.model_name}: {e}")
                # export_log.error_log += f"Error copying data for model {model._meta.model_name}: {e}\n"
                export_log.save()

    # try:
    #     with transaction.atomic(using='default'), \
    #          concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(copy_model_data, all_models)

    #     print("Data copying completed successfully!")
    try:
        with transaction.atomic(using='default'):
            for model in all_models:
                copy_model_data(model)

        print("Data copying completed successfully!")
    except Exception as e:
        print(f"Data copying failed: {e}")

class Application(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    invoice_code = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    license_type = models.CharField(max_length=255, null=True, blank=True)
    license_method = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    administrator = models.CharField(max_length=255, null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    version_control = models.IntegerField(default=1, editable=False)

    date_fields_to_convert = []
    integer_fields = ['quantity', ]                                                                                                                                                                                          
    float_fields = []

    def __str__(self):
        return self.name

    @property
    def is_parent(self):
        return self.application_set.exists()

# Change per install
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

class Image(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date_fields_to_convert = []
    integer_fields = []                                                                                                                                                                                          
    float_fields = []
    encrypted_fields = []

    def save(self, *args, **kwargs):
        if self.image:
            image = PILImage.open(self.image)
            raw_text = pytesseract.image_to_string(image)
            self.extracted_text = ', '.join(raw_text.split())
        super().save(*args, **kwargs)


class ImageLoader(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = QuillField(null=True, blank=True)
    recommendation = QuillField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    action_status = models.CharField(max_length=50, choices=ActionStatus.choices, default=ActionStatus.IS_ACTIVE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    deleted_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    version_control = models.IntegerField(default=1, editable=False)

    date_fields_to_convert = []
    integer_fields = []                                                                                                                                                                                          
    float_fields = []
    encrypted_fields = []

    @property
    def is_parent(self):
        return self.imageloader_set.exists()
    
class SelectedRows(models.Model):
    model = models.CharField(max_length=255)
    model_choice = models.CharField(max_length=255, choices=ModelChoices.choices)
    rows = models.TextField()
    favorite_id = models.TextField(null=True, blank=True)
    finding_id = models.TextField(null=True, blank=True)
    img_loader_id = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)
    tab_id = models.TextField(null=True, blank=True)

class SchemaAuditDatabaseUsers(models.Model):
    ID = models.AutoField(primary_key=True)
    SchemaAuditId = models.TextField(null=True, blank=True, verbose_name='SchemaAuditId', db_column='SchemaAuditId')
    When = models.BigIntegerField(null=True, blank=True, verbose_name='When', db_column='When')
    DatabaseName = models.TextField(null=True, blank=True, verbose_name='DatabaseName', db_column='DatabaseName')
    SystemUser = models.TextField(null=True, blank=True, verbose_name='SystemUser', db_column='SystemUser')
    UserName = models.TextField(null=True, blank=True, verbose_name='UserName', db_column='UserName')
    HostName = models.TextField(null=True, blank=True, verbose_name='HostName', db_column='HostName')
    OriginalUser = models.TextField(null=True, blank=True, verbose_name='OriginalUser', db_column='OriginalUser')
    EventType = models.TextField(null=True, blank=True, verbose_name='EventType', db_column='EventType')
    ObjectType = models.TextField(null=True, blank=True, verbose_name='ObjectType', db_column='ObjectType')
    ObjectName = models.TextField(null=True, blank=True, verbose_name='ObjectName', db_column='ObjectName')
    CommandText = models.TextField(null=True, blank=True, verbose_name='CommandText', db_column='CommandText')
    XMLEvent = models.TextField(null=True, blank=True, verbose_name='XMLEvent', db_column='XMLEvent')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['When',]
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class EmployeeListingApr25(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_Code = models.TextField(null=True, blank=True, verbose_name='Employee_Code', db_column='Employee_Code')
    Entity_Code = models.TextField(null=True, blank=True, verbose_name='Entity_Code', db_column='Entity_Code')
    Display_Name = models.TextField(null=True, blank=True, verbose_name='Display_Name', db_column='Display_Name')
    Date_Engaged = models.BigIntegerField(null=True, blank=True, verbose_name='Date_Engaged', db_column='Date_Engaged')
    Job_Grade = models.TextField(null=True, blank=True, verbose_name='Job_Grade', db_column='Job_Grade')
    Job_Title = models.TextField(null=True, blank=True, verbose_name='Job_Title', db_column='Job_Title')
    Employee_Status = models.TextField(null=True, blank=True, verbose_name='Employee_Status', db_column='Employee_Status')
    Company_Rule = models.TextField(null=True, blank=True, verbose_name='Company_Rule', db_column='Company_Rule')
    Termination_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Termination_Date', db_column='Termination_Date')
    Termination_Reason = models.TextField(null=True, blank=True, verbose_name='Termination_Reason', db_column='Termination_Reason')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    Gender = models.TextField(null=True, blank=True, verbose_name='Gender', db_column='Gender')
    Racial_Group = models.TextField(null=True, blank=True, verbose_name='Racial_Group', db_column='Racial_Group')
    Primary_Position = models.TextField(null=True, blank=True, verbose_name='Primary_Position', db_column='Primary_Position')
    Reports_To_Employee = models.TextField(null=True, blank=True, verbose_name='Reports_To_Employee', db_column='Reports_To_Employee')
    UIF_Status = models.TextField(null=True, blank=True, verbose_name='UIF_Status', db_column='UIF_Status')
    Nature_of_Contract = models.TextField(null=True, blank=True, verbose_name='Nature_of_Contract', db_column='Nature_of_Contract')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_Engaged', 'Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTUserActivitiesAuditResults284(models.Model):
    ID = models.AutoField(primary_key=True)
    Date = models.BigIntegerField(null=True, blank=True, verbose_name='Date', db_column='Date')
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    Role = models.TextField(null=True, blank=True, verbose_name='Role', db_column='Role')
    Record_Type = models.TextField(null=True, blank=True, verbose_name='Record_Type', db_column='Record_Type')
    Document_Number = models.TextField(null=True, blank=True, verbose_name='Document_Number', db_column='Document_Number')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTLoginAuditTrailResults676(models.Model):
    ID = models.AutoField(primary_key=True)
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Role = models.TextField(null=True, blank=True, verbose_name='Role', db_column='Role')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Last_Login = models.BigIntegerField(null=True, blank=True, verbose_name='Last_Login', db_column='Last_Login')
    IP_Address = models.TextField(null=True, blank=True, verbose_name='IP_Address', db_column='IP_Address')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Last_Login']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTListofActiveandInactiveUsersResults458(models.Model):
    ID = models.AutoField(primary_key=True)
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Role = models.TextField(null=True, blank=True, verbose_name='Role', db_column='Role')
    Inactive = models.TextField(null=True, blank=True, verbose_name='Inactive', db_column='Inactive')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class CopyofSLAhoursMay2025004(models.Model):
    ID = models.AutoField(primary_key=True)
    Date = models.BigIntegerField(null=True, blank=True, verbose_name='Date', db_column='Date')
    Employee = models.TextField(null=True, blank=True, verbose_name='Employee', db_column='Employee')
    Project = models.TextField(null=True, blank=True, verbose_name='Project', db_column='Project')
    Description = models.TextField(null=True, blank=True, verbose_name='Description', db_column='Description')
    Sales_Order_Item = models.TextField(null=True, blank=True, verbose_name='Sales_Order_Item', db_column='Sales_Order_Item')
    Validated_line = models.TextField(null=True, blank=True, verbose_name='Validated_line', db_column='Validated_line')
    Billable_Type = models.TextField(null=True, blank=True, verbose_name='Billable_Type', db_column='Billable_Type')
    Quantity = models.TextField(null=True, blank=True, verbose_name='Quantity', db_column='Quantity')
    Currency = models.TextField(null=True, blank=True, verbose_name='Currency', db_column='Currency')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class HRDataforITGeneralControlAudit(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True, verbose_name='Employee_First_Name', db_column='Employee_First_Name')
    Employee_Surname = models.TextField(null=True, blank=True, verbose_name='Employee_Surname', db_column='Employee_Surname')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Email_Address = models.TextField(null=True, blank=True, verbose_name='Email_Address', db_column='Email_Address')
    Date_Engaged = models.TextField(null=True, blank=True, verbose_name='Date_Engaged', db_column='Date_Engaged')
    Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='Date_Engaged_Converted', db_column='Date_Engaged_Converted')
    Contract_End_Date = models.TextField(null=True, blank=True, verbose_name='Contract_End_Date', db_column='Contract_End_Date')
    Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='Contract_End_Date_Converted', db_column='Contract_End_Date_Converted')
    Business_Title = models.TextField(null=True, blank=True, verbose_name='Business_Title', db_column='Business_Title')
    Reports_To = models.TextField(null=True, blank=True, verbose_name='Reports_To', db_column='Reports_To')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_Engaged_Converted', 'Contract_End_Date_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class InteractiveSignIns2025072120250722(models.Model):
    ID = models.AutoField(primary_key=True)
    Date_UTC = models.BigIntegerField(null=True, blank=True, verbose_name='Date_UTC', db_column='Date_UTC')
    Request_ID = models.TextField(null=True, blank=True, verbose_name='Request_ID', db_column='Request_ID')
    User_agent = models.TextField(null=True, blank=True, verbose_name='User_agent', db_column='User_agent')
    Correlation_ID = models.TextField(null=True, blank=True, verbose_name='Correlation_ID', db_column='Correlation_ID')
    User_ID = models.TextField(null=True, blank=True, verbose_name='User_ID', db_column='User_ID')
    User = models.TextField(null=True, blank=True, verbose_name='User', db_column='User')
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    Authentication_Protocol = models.TextField(null=True, blank=True, verbose_name='Authentication_Protocol', db_column='Authentication_Protocol')
    Unique_token_identifier = models.TextField(null=True, blank=True, verbose_name='Unique_token_identifier', db_column='Unique_token_identifier')
    Original_transfer_method = models.TextField(null=True, blank=True, verbose_name='Original_transfer_method', db_column='Original_transfer_method')
    Token_Protection_Sign_In_Session = models.TextField(null=True, blank=True, verbose_name='Token_Protection_Sign_In_Session', db_column='Token_Protection_Sign_In_Session')
    Token_Protection_Sign_In_Session_StatusCode = models.TextField(null=True, blank=True, verbose_name='Token_Protection_Sign_In_Session_StatusCode', db_column='Token_Protection_Sign_In_Session_StatusCode')
    Application = models.TextField(null=True, blank=True, verbose_name='Application', db_column='Application')
    Application_ID = models.TextField(null=True, blank=True, verbose_name='Application_ID', db_column='Application_ID')
    App_owner_tenant_ID = models.TextField(null=True, blank=True, verbose_name='App_owner_tenant_ID', db_column='App_owner_tenant_ID')
    Resource = models.TextField(null=True, blank=True, verbose_name='Resource', db_column='Resource')
    Resource_ID = models.TextField(null=True, blank=True, verbose_name='Resource_ID', db_column='Resource_ID')
    Resource_tenant_ID = models.TextField(null=True, blank=True, verbose_name='Resource_tenant_ID', db_column='Resource_tenant_ID')
    Resource_owner_tenant_ID = models.TextField(null=True, blank=True, verbose_name='Resource_owner_tenant_ID', db_column='Resource_owner_tenant_ID')
    Home_tenant_ID = models.TextField(null=True, blank=True, verbose_name='Home_tenant_ID', db_column='Home_tenant_ID')
    Home_tenant_name = models.TextField(null=True, blank=True, verbose_name='Home_tenant_name', db_column='Home_tenant_name')
    IP_address = models.TextField(null=True, blank=True, verbose_name='IP_address', db_column='IP_address')
    Location = models.TextField(null=True, blank=True, verbose_name='Location', db_column='Location')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Signin_error_code = models.TextField(null=True, blank=True, verbose_name='Signin_error_code', db_column='Signin_error_code')
    Failure_reason = models.TextField(null=True, blank=True, verbose_name='Failure_reason', db_column='Failure_reason')
    Client_app = models.TextField(null=True, blank=True, verbose_name='Client_app', db_column='Client_app')
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Browser = models.TextField(null=True, blank=True, verbose_name='Browser', db_column='Browser')
    Operating_System = models.TextField(null=True, blank=True, verbose_name='Operating_System', db_column='Operating_System')
    Compliant = models.TextField(null=True, blank=True, verbose_name='Compliant', db_column='Compliant')
    Managed = models.TextField(null=True, blank=True, verbose_name='Managed', db_column='Managed')
    Join_Type = models.TextField(null=True, blank=True, verbose_name='Join_Type', db_column='Join_Type')
    Multifactor_authentication_result = models.TextField(null=True, blank=True, verbose_name='Multifactor_authentication_result', db_column='Multifactor_authentication_result')
    Multifactor_authentication_auth_method = models.TextField(null=True, blank=True, verbose_name='Multifactor_authentication_auth_method', db_column='Multifactor_authentication_auth_method')
    Multifactor_authentication_auth_detail = models.TextField(null=True, blank=True, verbose_name='Multifactor_authentication_auth_detail', db_column='Multifactor_authentication_auth_detail')
    Authentication_requirement = models.TextField(null=True, blank=True, verbose_name='Authentication_requirement', db_column='Authentication_requirement')
    Signin_identifier = models.TextField(null=True, blank=True, verbose_name='Signin_identifier', db_column='Signin_identifier')
    Session_ID = models.TextField(null=True, blank=True, verbose_name='Session_ID', db_column='Session_ID')
    IP_address_seen_by_resource = models.TextField(null=True, blank=True, verbose_name='IP_address_seen_by_resource', db_column='IP_address_seen_by_resource')
    Through_Global_Secure_Access = models.TextField(null=True, blank=True, verbose_name='Through_Global_Secure_Access', db_column='Through_Global_Secure_Access')
    Global_Secure_Access_IP_address = models.TextField(null=True, blank=True, verbose_name='Global_Secure_Access_IP_address', db_column='Global_Secure_Access_IP_address')
    Autonomous_system_number = models.TextField(null=True, blank=True, verbose_name='Autonomous_system_number', db_column='Autonomous_system_number')
    Flagged_for_review = models.TextField(null=True, blank=True, verbose_name='Flagged_for_review', db_column='Flagged_for_review')
    Token_issuer_name = models.TextField(null=True, blank=True, verbose_name='Token_issuer_name', db_column='Token_issuer_name')
    Latency = models.TextField(null=True, blank=True, verbose_name='Latency', db_column='Latency')
    Conditional_Access = models.TextField(null=True, blank=True, verbose_name='Conditional_Access', db_column='Conditional_Access')
    Associated_Resource_Id = models.TextField(null=True, blank=True, verbose_name='Associated_Resource_Id', db_column='Associated_Resource_Id')
    Federated_Token_Id = models.TextField(null=True, blank=True, verbose_name='Federated_Token_Id', db_column='Federated_Token_Id')
    Federated_Token_Issuer = models.TextField(null=True, blank=True, verbose_name='Federated_Token_Issuer', db_column='Federated_Token_Issuer')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_UTC']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTHRListVsActiveInactiveList(models.Model):
    ID = models.AutoField(primary_key=True)
    Username = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    Role = models.TextField(null=True, blank=True)
    Inactive = models.TextField(null=True, blank=True)
    d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Email_Address = models.TextField(null=True, blank=True)
    d_Date_Engaged = models.TextField(null=True, blank=True)
    d_Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    d_Contract_End_Date = models.TextField(null=True, blank=True)
    d_Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    d_Business_Title = models.TextField(null=True, blank=True)
    d_Reports_To = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 1  # Do not change this value
    date_fields_to_convert = ['d_Date_Engaged_Converted', 'd_Contract_End_Date_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTHRListVsActiveInactiveList01(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Email_Address = models.TextField(null=True, blank=True)
    Date_Engaged = models.TextField(null=True, blank=True)
    Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    Contract_End_Date = models.TextField(null=True, blank=True)
    Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_Role = models.TextField(null=True, blank=True)
    d_Inactive = models.TextField(null=True, blank=True)
    d_d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_d_Employee_Surname = models.TextField(null=True, blank=True)
    d_d_Department = models.TextField(null=True, blank=True)
    d_d_Email_Address = models.TextField(null=True, blank=True)
    d_d_Date_Engaged = models.TextField(null=True, blank=True)
    d_d_Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    d_d_Contract_End_Date = models.TextField(null=True, blank=True)
    d_d_Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    d_d_Business_Title = models.TextField(null=True, blank=True)
    d_d_Reports_To = models.TextField(null=True, blank=True)
    d_both = models.IntegerField(null=True, blank=True)
    d_base = models.IntegerField(null=True, blank=True)
    d_delta = models.IntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 2  # Do not change this value
    date_fields_to_convert = ['d_d_Contract_End_Date_Converted', 'Contract_End_Date_Converted', 'Date_Engaged_Converted', 'd_d_Date_Engaged_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTHRListVsActiveInactiveList02(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Email_Address = models.TextField(null=True, blank=True)
    Date_Engaged = models.TextField(null=True, blank=True)
    Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    Contract_End_Date = models.TextField(null=True, blank=True)
    Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_Role = models.TextField(null=True, blank=True)
    d_Inactive = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 3  # Do not change this value
    date_fields_to_convert = ['Contract_End_Date_Converted', 'Date_Engaged_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTHRListVsActiveInactiveList03(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Email_Address = models.TextField(null=True, blank=True)
    Date_Engaged = models.TextField(null=True, blank=True)
    Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    Contract_End_Date = models.TextField(null=True, blank=True)
    Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_Role = models.TextField(null=True, blank=True)
    d_Inactive = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 4  # Do not change this value
    date_fields_to_convert = ['Contract_End_Date_Converted', 'Date_Engaged_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class LoginAuditTrailResultsVSAHTHRList(models.Model):
    ID = models.AutoField(primary_key=True)
    Username = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    Role = models.TextField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Last_Login = models.BigIntegerField(null=True, blank=True)
    IP_Address = models.TextField(null=True, blank=True)
    d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Email_Address = models.TextField(null=True, blank=True)
    d_Date_Engaged = models.TextField(null=True, blank=True)
    d_Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    d_Contract_End_Date = models.TextField(null=True, blank=True)
    d_Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    d_Business_Title = models.TextField(null=True, blank=True)
    d_Reports_To = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 5  # Do not change this value
    date_fields_to_convert = ['Last_Login', 'd_Date_Engaged_Converted', 'd_Contract_End_Date_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTUserActivitiesAuditResultsVSAHTHRList(models.Model):
    ID = models.AutoField(primary_key=True)
    Date = models.BigIntegerField(null=True, blank=True)
    Username = models.TextField(null=True, blank=True)
    Role = models.TextField(null=True, blank=True)
    Record_Type = models.TextField(null=True, blank=True)
    Document_Number = models.TextField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Email_Address = models.TextField(null=True, blank=True)
    d_Date_Engaged = models.TextField(null=True, blank=True)
    d_Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    d_Contract_End_Date = models.TextField(null=True, blank=True)
    d_Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    d_Business_Title = models.TextField(null=True, blank=True)
    d_Reports_To = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 6  # Do not change this value
    date_fields_to_convert = ['d_Contract_End_Date_Converted', 'd_Date_Engaged_Converted', 'Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class NetsuiteAHTSandboxEmployeeSearchActiveandInactiveResults(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Job_Title = models.TextField(null=True, blank=True, verbose_name='Job_Title', db_column='Job_Title')
    Role = models.TextField(null=True, blank=True, verbose_name='Role', db_column='Role')
    Date_Created = models.BigIntegerField(null=True, blank=True, verbose_name='Date_Created', db_column='Date_Created')
    Inactive = models.TextField(null=True, blank=True, verbose_name='Inactive', db_column='Inactive')
    Login_Access = models.TextField(null=True, blank=True, verbose_name='Login_Access', db_column='Login_Access')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_Created']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class NetsuiteAHTProductionEmployeeSearchActiveandInactive(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Job_Title = models.TextField(null=True, blank=True, verbose_name='Job_Title', db_column='Job_Title')
    Role = models.TextField(null=True, blank=True, verbose_name='Role', db_column='Role')
    Date_Created = models.BigIntegerField(null=True, blank=True, verbose_name='Date_Created', db_column='Date_Created')
    Inactive = models.TextField(null=True, blank=True, verbose_name='Inactive', db_column='Inactive')
    Login_Access = models.TextField(null=True, blank=True, verbose_name='Login_Access', db_column='Login_Access')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_Created']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTHelpdeskTickets(models.Model):
    ID = models.AutoField(primary_key=True)
    Activities = models.TextField(null=True, blank=True, verbose_name='Activities', db_column='Activities')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Assigned_to = models.TextField(null=True, blank=True, verbose_name='Assigned_to', db_column='Assigned_to')
    Close_date = models.BigIntegerField(null=True, blank=True, verbose_name='Close_date', db_column='Close_date')
    Created_on = models.BigIntegerField(null=True, blank=True, verbose_name='Created_on', db_column='Created_on')
    Customer = models.TextField(null=True, blank=True, verbose_name='Customer', db_column='Customer')
    Helpdesk_Team = models.TextField(null=True, blank=True, verbose_name='Helpdesk_Team', db_column='Helpdesk_Team')
    Kanban_State = models.TextField(null=True, blank=True, verbose_name='Kanban_State', db_column='Kanban_State')
    Last_Updated_on = models.BigIntegerField(null=True, blank=True, verbose_name='Last_Updated_on', db_column='Last_Updated_on')
    Originator_Email = models.TextField(null=True, blank=True, verbose_name='Originator_Email', db_column='Originator_Email')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Stage = models.TextField(null=True, blank=True, verbose_name='Stage', db_column='Stage')
    Subject = models.TextField(null=True, blank=True, verbose_name='Subject', db_column='Subject')
    Ticket_IDs_Sequence = models.IntegerField(null=True, blank=True, verbose_name='Ticket_IDs_Sequence', db_column='Ticket_IDs_Sequence')
    Ticket_Type = models.TextField(null=True, blank=True, verbose_name='Ticket_Type', db_column='Ticket_Type')
    Time_Spent = models.FloatField(null=True, blank=True, verbose_name='Time_Spent', db_column='Time_Spent')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Close_date', 'Created_on', 'Last_Updated_on']
    integer_fields = ['Ticket_IDs_Sequence']
    float_fields = ['Time_Spent']
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DataforITGeneralControlAuditTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True, verbose_name='Employee_First_Name', db_column='Employee_First_Name')
    Employee_Surname = models.TextField(null=True, blank=True, verbose_name='Employee_Surname', db_column='Employee_Surname')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Termination_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Termination_Date', db_column='Termination_Date')
    Business_Title = models.TextField(null=True, blank=True, verbose_name='Business_Title', db_column='Business_Title')
    Reports_To = models.TextField(null=True, blank=True, verbose_name='Reports_To', db_column='Reports_To')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class TerminationsVSActiveInactive(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Termination_Date = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_Role = models.TextField(null=True, blank=True)
    d_Inactive = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 7  # Do not change this value
    date_fields_to_convert = ['Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class TerminationsVSHR(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Termination_Date = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Email_Address = models.TextField(null=True, blank=True)
    d_Date_Engaged = models.TextField(null=True, blank=True)
    d_Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    d_Contract_End_Date = models.TextField(null=True, blank=True)
    d_Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    d_Business_Title = models.TextField(null=True, blank=True)
    d_Reports_To = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 8  # Do not change this value
    date_fields_to_convert = ['Termination_Date', 'd_Date_Engaged_Converted', 'd_Contract_End_Date_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaTerminationsVSHR(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Termination_Date = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Email_Address = models.TextField(null=True, blank=True)
    d_Date_Engaged = models.TextField(null=True, blank=True)
    d_Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    d_Contract_End_Date = models.TextField(null=True, blank=True)
    d_Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    d_Business_Title = models.TextField(null=True, blank=True)
    d_Reports_To = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 9  # Do not change this value
    date_fields_to_convert = ['Termination_Date', 'd_Date_Engaged_Converted', 'd_Contract_End_Date_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaHRVSNetsuiteProd(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Email_Address = models.TextField(null=True, blank=True)
    Date_Engaged = models.TextField(null=True, blank=True)
    Date_Engaged_Converted = models.BigIntegerField(null=True, blank=True)
    Contract_End_Date = models.TextField(null=True, blank=True)
    Contract_End_Date_Converted = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Role = models.TextField(null=True, blank=True)
    d_Date_Created = models.BigIntegerField(null=True, blank=True)
    d_Inactive = models.TextField(null=True, blank=True)
    d_Login_Access = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 10  # Do not change this value
    date_fields_to_convert = ['d_Date_Created', 'Date_Engaged_Converted', 'Contract_End_Date_Converted']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaTerminationsVSNetsuiteProd(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Termination_Date = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Role = models.TextField(null=True, blank=True)
    d_Date_Created = models.BigIntegerField(null=True, blank=True)
    d_Inactive = models.TextField(null=True, blank=True)
    d_Login_Access = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 11  # Do not change this value
    date_fields_to_convert = ['d_Date_Created', 'Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []

class ADSAV(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    UPN = models.TextField(null=True, blank=True, verbose_name='UPN', db_column='UPN')
    ReportStatus = models.TextField(null=True, blank=True, verbose_name='ReportStatus', db_column='ReportStatus')
    ReportStatus_loc = models.TextField(null=True, blank=True, verbose_name='ReportStatus_loc', db_column='ReportStatus_loc')
    AssignmentFilterIds = models.TextField(null=True, blank=True, verbose_name='AssignmentFilterIds', db_column='AssignmentFilterIds')
    PspdpuLastModifiedTimeUtc = models.BigIntegerField(null=True, blank=True, verbose_name='PspdpuLastModifiedTimeUtc', db_column='PspdpuLastModifiedTimeUtc')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['PspdpuLastModifiedTimeUtc']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Managed_by = models.TextField(null=True, blank=True, verbose_name='Managed_by', db_column='Managed_by')
    Ownership = models.TextField(null=True, blank=True, verbose_name='Ownership', db_column='Ownership')
    Compliance = models.TextField(null=True, blank=True, verbose_name='Compliance', db_column='Compliance')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    Device_state = models.TextField(null=True, blank=True, verbose_name='Device_state', db_column='Device_state')
    Primary_user_email_address = models.TextField(null=True, blank=True, verbose_name='Primary_user_email_address', db_column='Primary_user_email_address')
    Primary_user_UPN = models.TextField(null=True, blank=True, verbose_name='Primary_user_UPN', db_column='Primary_user_UPN')
    Last_checkin = models.BigIntegerField(null=True, blank=True, verbose_name='Last_checkin', db_column='Last_checkin')
    Category = models.TextField(null=True, blank=True, verbose_name='Category', db_column='Category')
    Encrypted = models.TextField(null=True, blank=True, verbose_name='Encrypted', db_column='Encrypted')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    Manufacturer = models.TextField(null=True, blank=True, verbose_name='Manufacturer', db_column='Manufacturer')
    Serial_number = models.TextField(null=True, blank=True, verbose_name='Serial_number', db_column='Serial_number')
    Management_name = models.TextField(null=True, blank=True, verbose_name='Management_name', db_column='Management_name')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Last_checkin']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTAV(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    UPN = models.TextField(null=True, blank=True, verbose_name='UPN', db_column='UPN')
    ReportStatus = models.TextField(null=True, blank=True, verbose_name='ReportStatus', db_column='ReportStatus')
    ReportStatus_loc = models.TextField(null=True, blank=True, verbose_name='ReportStatus_loc', db_column='ReportStatus_loc')
    AssignmentFilterIds = models.TextField(null=True, blank=True, verbose_name='AssignmentFilterIds', db_column='AssignmentFilterIds')
    PspdpuLastModifiedTimeUtc = models.BigIntegerField(null=True, blank=True, verbose_name='PspdpuLastModifiedTimeUtc', db_column='PspdpuLastModifiedTimeUtc')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['PspdpuLastModifiedTimeUtc']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTDefender(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_Name = models.TextField(null=True, blank=True, verbose_name='Device_Name', db_column='Device_Name')
    Device_Category = models.TextField(null=True, blank=True, verbose_name='Device_Category', db_column='Device_Category')
    Device_Type = models.TextField(null=True, blank=True, verbose_name='Device_Type', db_column='Device_Type')
    Device_Subtype = models.TextField(null=True, blank=True, verbose_name='Device_Subtype', db_column='Device_Subtype')
    Discovery_sources = models.TextField(null=True, blank=True, verbose_name='Discovery_sources', db_column='Discovery_sources')
    Domain = models.TextField(null=True, blank=True, verbose_name='Domain', db_column='Domain')
    AAD_Device_Id = models.TextField(null=True, blank=True, verbose_name='AAD_Device_Id', db_column='AAD_Device_Id')
    First_Seen = models.BigIntegerField(null=True, blank=True, verbose_name='First_Seen', db_column='First_Seen')
    Last_device_update = models.BigIntegerField(null=True, blank=True, verbose_name='Last_device_update', db_column='Last_device_update')
    OS_Platform = models.TextField(null=True, blank=True, verbose_name='OS_Platform', db_column='OS_Platform')
    OS_Distribution = models.TextField(null=True, blank=True, verbose_name='OS_Distribution', db_column='OS_Distribution')
    OS_Version = models.TextField(null=True, blank=True, verbose_name='OS_Version', db_column='OS_Version')
    OS_Build = models.TextField(null=True, blank=True, verbose_name='OS_Build', db_column='OS_Build')
    Windows_10_Version = models.TextField(null=True, blank=True, verbose_name='Windows_10_Version', db_column='Windows_10_Version')
    Tags = models.TextField(null=True, blank=True, verbose_name='Tags', db_column='Tags')
    Group = models.TextField(null=True, blank=True, verbose_name='Group', db_column='Group')
    Is_AAD_Joined = models.TextField(null=True, blank=True, verbose_name='Is_AAD_Joined', db_column='Is_AAD_Joined')
    Device_IPs = models.TextField(null=True, blank=True, verbose_name='Device_IPs', db_column='Device_IPs')
    Device_MACs = models.TextField(null=True, blank=True, verbose_name='Device_MACs', db_column='Device_MACs')
    Risk_Level = models.TextField(null=True, blank=True, verbose_name='Risk_Level', db_column='Risk_Level')
    Exposure_Level = models.TextField(null=True, blank=True, verbose_name='Exposure_Level', db_column='Exposure_Level')
    Health_Status = models.TextField(null=True, blank=True, verbose_name='Health_Status', db_column='Health_Status')
    Onboarding_Status = models.TextField(null=True, blank=True, verbose_name='Onboarding_Status', db_column='Onboarding_Status')
    Device_Role = models.TextField(null=True, blank=True, verbose_name='Device_Role', db_column='Device_Role')
    Cloud_Platforms = models.TextField(null=True, blank=True, verbose_name='Cloud_Platforms', db_column='Cloud_Platforms')
    Is_Internet_Facing = models.TextField(null=True, blank=True, verbose_name='Is_Internet_Facing', db_column='Is_Internet_Facing')
    Enrollment_Status_Code = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status_Code', db_column='Enrollment_Status_Code')
    Managed_By = models.TextField(null=True, blank=True, verbose_name='Managed_By', db_column='Managed_By')
    Enrollment_Status = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status', db_column='Enrollment_Status')
    Vendor = models.TextField(null=True, blank=True, verbose_name='Vendor', db_column='Vendor')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    Firmware_versions = models.TextField(null=True, blank=True, verbose_name='Firmware_versions', db_column='Firmware_versions')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['First_Seen', 'Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ASECDevicesDefender(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_Name = models.TextField(null=True, blank=True, verbose_name='Device_Name', db_column='Device_Name')
    Device_Category = models.TextField(null=True, blank=True, verbose_name='Device_Category', db_column='Device_Category')
    Device_Type = models.TextField(null=True, blank=True, verbose_name='Device_Type', db_column='Device_Type')
    Device_Subtype = models.TextField(null=True, blank=True, verbose_name='Device_Subtype', db_column='Device_Subtype')
    Discovery_sources = models.TextField(null=True, blank=True, verbose_name='Discovery_sources', db_column='Discovery_sources')
    Domain = models.TextField(null=True, blank=True, verbose_name='Domain', db_column='Domain')
    AAD_Device_Id = models.TextField(null=True, blank=True, verbose_name='AAD_Device_Id', db_column='AAD_Device_Id')
    First_Seen = models.BigIntegerField(null=True, blank=True, verbose_name='First_Seen', db_column='First_Seen')
    Last_device_update = models.BigIntegerField(null=True, blank=True, verbose_name='Last_device_update', db_column='Last_device_update')
    OS_Platform = models.TextField(null=True, blank=True, verbose_name='OS_Platform', db_column='OS_Platform')
    OS_Distribution = models.TextField(null=True, blank=True, verbose_name='OS_Distribution', db_column='OS_Distribution')
    OS_Version = models.TextField(null=True, blank=True, verbose_name='OS_Version', db_column='OS_Version')
    OS_Build = models.TextField(null=True, blank=True, verbose_name='OS_Build', db_column='OS_Build')
    Windows_10_Version = models.TextField(null=True, blank=True, verbose_name='Windows_10_Version', db_column='Windows_10_Version')
    Tags = models.TextField(null=True, blank=True, verbose_name='Tags', db_column='Tags')
    Group = models.TextField(null=True, blank=True, verbose_name='Group', db_column='Group')
    Is_AAD_Joined = models.TextField(null=True, blank=True, verbose_name='Is_AAD_Joined', db_column='Is_AAD_Joined')
    Device_IPs = models.TextField(null=True, blank=True, verbose_name='Device_IPs', db_column='Device_IPs')
    Device_MACs = models.TextField(null=True, blank=True, verbose_name='Device_MACs', db_column='Device_MACs')
    Risk_Level = models.TextField(null=True, blank=True, verbose_name='Risk_Level', db_column='Risk_Level')
    Exposure_Level = models.TextField(null=True, blank=True, verbose_name='Exposure_Level', db_column='Exposure_Level')
    Health_Status = models.TextField(null=True, blank=True, verbose_name='Health_Status', db_column='Health_Status')
    Onboarding_Status = models.TextField(null=True, blank=True, verbose_name='Onboarding_Status', db_column='Onboarding_Status')
    Device_Role = models.TextField(null=True, blank=True, verbose_name='Device_Role', db_column='Device_Role')
    Cloud_Platforms = models.TextField(null=True, blank=True, verbose_name='Cloud_Platforms', db_column='Cloud_Platforms')
    Is_Internet_Facing = models.TextField(null=True, blank=True, verbose_name='Is_Internet_Facing', db_column='Is_Internet_Facing')
    Enrollment_Status_Code = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status_Code', db_column='Enrollment_Status_Code')
    Managed_By = models.TextField(null=True, blank=True, verbose_name='Managed_By', db_column='Managed_By')
    Enrollment_Status = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status', db_column='Enrollment_Status')
    Vendor = models.TextField(null=True, blank=True, verbose_name='Vendor', db_column='Vendor')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    Firmware_versions = models.TextField(null=True, blank=True, verbose_name='Firmware_versions', db_column='Firmware_versions')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['First_Seen', 'Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ASECAV(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    UPN = models.TextField(null=True, blank=True, verbose_name='UPN', db_column='UPN')
    ReportStatus = models.TextField(null=True, blank=True, verbose_name='ReportStatus', db_column='ReportStatus')
    ReportStatus_loc = models.TextField(null=True, blank=True, verbose_name='ReportStatus_loc', db_column='ReportStatus_loc')
    AssignmentFilterIds = models.TextField(null=True, blank=True, verbose_name='AssignmentFilterIds', db_column='AssignmentFilterIds')
    PspdpuLastModifiedTimeUtc = models.BigIntegerField(null=True, blank=True, verbose_name='PspdpuLastModifiedTimeUtc', db_column='PspdpuLastModifiedTimeUtc')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['PspdpuLastModifiedTimeUtc']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ASECIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Enrollment_date = models.BigIntegerField(null=True, blank=True, verbose_name='Enrollment_date', db_column='Enrollment_date')
    Last_checkin = models.BigIntegerField(null=True, blank=True, verbose_name='Last_checkin', db_column='Last_checkin')
    Azure_AD_Device_ID = models.TextField(null=True, blank=True, verbose_name='Azure_AD_Device_ID', db_column='Azure_AD_Device_ID')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    Azure_AD_registered = models.TextField(null=True, blank=True, verbose_name='Azure_AD_registered', db_column='Azure_AD_registered')
    EAS_activation_ID = models.TextField(null=True, blank=True, verbose_name='EAS_activation_ID', db_column='EAS_activation_ID')
    Serial_number = models.TextField(null=True, blank=True, verbose_name='Serial_number', db_column='Serial_number')
    Manufacturer = models.TextField(null=True, blank=True, verbose_name='Manufacturer', db_column='Manufacturer')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    EAS_activated = models.TextField(null=True, blank=True, verbose_name='EAS_activated', db_column='EAS_activated')
    IMEI = models.TextField(null=True, blank=True, verbose_name='IMEI', db_column='IMEI')
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True, verbose_name='Last_EAS_sync_time', db_column='Last_EAS_sync_time')
    EAS_reason = models.TextField(null=True, blank=True, verbose_name='EAS_reason', db_column='EAS_reason')
    EAS_status = models.TextField(null=True, blank=True, verbose_name='EAS_status', db_column='EAS_status')
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True, verbose_name='Compliance_grace_period_expiration', db_column='Compliance_grace_period_expiration')
    Security_patch_level = models.TextField(null=True, blank=True, verbose_name='Security_patch_level', db_column='Security_patch_level')
    WiFi_MAC = models.TextField(null=True, blank=True, verbose_name='WiFi_MAC', db_column='WiFi_MAC')
    MEID = models.TextField(null=True, blank=True, verbose_name='MEID', db_column='MEID')
    Subscriber_carrier = models.TextField(null=True, blank=True, verbose_name='Subscriber_carrier', db_column='Subscriber_carrier')
    Total_storage = models.TextField(null=True, blank=True, verbose_name='Total_storage', db_column='Total_storage')
    Free_storage = models.TextField(null=True, blank=True, verbose_name='Free_storage', db_column='Free_storage')
    Management_name = models.TextField(null=True, blank=True, verbose_name='Management_name', db_column='Management_name')
    Category = models.TextField(null=True, blank=True, verbose_name='Category', db_column='Category')
    UserId = models.TextField(null=True, blank=True, verbose_name='UserId', db_column='UserId')
    Primary_user_UPN = models.TextField(null=True, blank=True, verbose_name='Primary_user_UPN', db_column='Primary_user_UPN')
    Primary_user_email_address = models.TextField(null=True, blank=True, verbose_name='Primary_user_email_address', db_column='Primary_user_email_address')
    Primary_user_display_name = models.TextField(null=True, blank=True, verbose_name='Primary_user_display_name', db_column='Primary_user_display_name')
    WiFiIPv4Address = models.TextField(null=True, blank=True, verbose_name='WiFiIPv4Address', db_column='WiFiIPv4Address')
    WiFiSubnetID = models.TextField(null=True, blank=True, verbose_name='WiFiSubnetID', db_column='WiFiSubnetID')
    Compliance = models.TextField(null=True, blank=True, verbose_name='Compliance', db_column='Compliance')
    Managed_by = models.TextField(null=True, blank=True, verbose_name='Managed_by', db_column='Managed_by')
    Ownership = models.TextField(null=True, blank=True, verbose_name='Ownership', db_column='Ownership')
    Device_state = models.TextField(null=True, blank=True, verbose_name='Device_state', db_column='Device_state')
    Intune_registered = models.TextField(null=True, blank=True, verbose_name='Intune_registered', db_column='Intune_registered')
    Supervised = models.TextField(null=True, blank=True, verbose_name='Supervised', db_column='Supervised')
    Encrypted = models.TextField(null=True, blank=True, verbose_name='Encrypted', db_column='Encrypted')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    SkuFamily = models.TextField(null=True, blank=True, verbose_name='SkuFamily', db_column='SkuFamily')
    JoinType = models.TextField(null=True, blank=True, verbose_name='JoinType', db_column='JoinType')
    Phone_number = models.TextField(null=True, blank=True, verbose_name='Phone_number', db_column='Phone_number')
    Jailbroken = models.TextField(null=True, blank=True, verbose_name='Jailbroken', db_column='Jailbroken')
    ICCID = models.TextField(null=True, blank=True, verbose_name='ICCID', db_column='ICCID')
    EthernetMAC = models.TextField(null=True, blank=True, verbose_name='EthernetMAC', db_column='EthernetMAC')
    CellularTechnology = models.TextField(null=True, blank=True, verbose_name='CellularTechnology', db_column='CellularTechnology')
    ProcessorArchitecture = models.TextField(null=True, blank=True, verbose_name='ProcessorArchitecture', db_column='ProcessorArchitecture')
    EID = models.TextField(null=True, blank=True, verbose_name='EID', db_column='EID')
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True, verbose_name='SystemManagementBIOSVersion', db_column='SystemManagementBIOSVersion')
    TPMManufacturerId = models.TextField(null=True, blank=True, verbose_name='TPMManufacturerId', db_column='TPMManufacturerId')
    TPMManufacturerVersion = models.TextField(null=True, blank=True, verbose_name='TPMManufacturerVersion', db_column='TPMManufacturerVersion')
    ProductName = models.TextField(null=True, blank=True, verbose_name='ProductName', db_column='ProductName')
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True, verbose_name='Management_certificate_expiration_date', db_column='Management_certificate_expiration_date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Enrollment_date', 'Last_checkin', 'Last_EAS_sync_time', 'Compliance_grace_period_expiration', 'Management_certificate_expiration_date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class NupayAV(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    UPN = models.TextField(null=True, blank=True, verbose_name='UPN', db_column='UPN')
    ReportStatus = models.TextField(null=True, blank=True, verbose_name='ReportStatus', db_column='ReportStatus')
    ReportStatus_loc = models.TextField(null=True, blank=True, verbose_name='ReportStatus_loc', db_column='ReportStatus_loc')
    AssignmentFilterIds = models.TextField(null=True, blank=True, verbose_name='AssignmentFilterIds', db_column='AssignmentFilterIds')
    PspdpuLastModifiedTimeUtc = models.BigIntegerField(null=True, blank=True, verbose_name='PspdpuLastModifiedTimeUtc', db_column='PspdpuLastModifiedTimeUtc')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['PspdpuLastModifiedTimeUtc']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class NupayDefender(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_Name = models.TextField(null=True, blank=True, verbose_name='Device_Name', db_column='Device_Name')
    Device_Category = models.TextField(null=True, blank=True, verbose_name='Device_Category', db_column='Device_Category')
    Device_Type = models.TextField(null=True, blank=True, verbose_name='Device_Type', db_column='Device_Type')
    Device_Subtype = models.TextField(null=True, blank=True, verbose_name='Device_Subtype', db_column='Device_Subtype')
    Discovery_sources = models.TextField(null=True, blank=True, verbose_name='Discovery_sources', db_column='Discovery_sources')
    Domain = models.TextField(null=True, blank=True, verbose_name='Domain', db_column='Domain')
    AAD_Device_Id = models.TextField(null=True, blank=True, verbose_name='AAD_Device_Id', db_column='AAD_Device_Id')
    First_Seen = models.BigIntegerField(null=True, blank=True, verbose_name='First_Seen', db_column='First_Seen')
    Last_device_update = models.BigIntegerField(null=True, blank=True, verbose_name='Last_device_update', db_column='Last_device_update')
    OS_Platform = models.TextField(null=True, blank=True, verbose_name='OS_Platform', db_column='OS_Platform')
    OS_Distribution = models.TextField(null=True, blank=True, verbose_name='OS_Distribution', db_column='OS_Distribution')
    OS_Version = models.TextField(null=True, blank=True, verbose_name='OS_Version', db_column='OS_Version')
    OS_Build = models.TextField(null=True, blank=True, verbose_name='OS_Build', db_column='OS_Build')
    Windows_10_Version = models.TextField(null=True, blank=True, verbose_name='Windows_10_Version', db_column='Windows_10_Version')
    Tags = models.TextField(null=True, blank=True, verbose_name='Tags', db_column='Tags')
    Group = models.TextField(null=True, blank=True, verbose_name='Group', db_column='Group')
    Is_AAD_Joined = models.TextField(null=True, blank=True, verbose_name='Is_AAD_Joined', db_column='Is_AAD_Joined')
    Device_IPs = models.TextField(null=True, blank=True, verbose_name='Device_IPs', db_column='Device_IPs')
    Device_MACs = models.TextField(null=True, blank=True, verbose_name='Device_MACs', db_column='Device_MACs')
    Risk_Level = models.TextField(null=True, blank=True, verbose_name='Risk_Level', db_column='Risk_Level')
    Exposure_Level = models.TextField(null=True, blank=True, verbose_name='Exposure_Level', db_column='Exposure_Level')
    Health_Status = models.TextField(null=True, blank=True, verbose_name='Health_Status', db_column='Health_Status')
    Onboarding_Status = models.TextField(null=True, blank=True, verbose_name='Onboarding_Status', db_column='Onboarding_Status')
    Device_Role = models.TextField(null=True, blank=True, verbose_name='Device_Role', db_column='Device_Role')
    Cloud_Platforms = models.TextField(null=True, blank=True, verbose_name='Cloud_Platforms', db_column='Cloud_Platforms')
    Is_Internet_Facing = models.TextField(null=True, blank=True, verbose_name='Is_Internet_Facing', db_column='Is_Internet_Facing')
    Enrollment_Status_Code = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status_Code', db_column='Enrollment_Status_Code')
    Managed_By = models.TextField(null=True, blank=True, verbose_name='Managed_By', db_column='Managed_By')
    Enrollment_Status = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status', db_column='Enrollment_Status')
    Vendor = models.TextField(null=True, blank=True, verbose_name='Vendor', db_column='Vendor')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    Firmware_versions = models.TextField(null=True, blank=True, verbose_name='Firmware_versions', db_column='Firmware_versions')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['First_Seen', 'Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class NupayIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Enrollment_date = models.BigIntegerField(null=True, blank=True, verbose_name='Enrollment_date', db_column='Enrollment_date')
    Last_checkin = models.BigIntegerField(null=True, blank=True, verbose_name='Last_checkin', db_column='Last_checkin')
    Azure_AD_Device_ID = models.TextField(null=True, blank=True, verbose_name='Azure_AD_Device_ID', db_column='Azure_AD_Device_ID')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    Azure_AD_registered = models.TextField(null=True, blank=True, verbose_name='Azure_AD_registered', db_column='Azure_AD_registered')
    EAS_activation_ID = models.TextField(null=True, blank=True, verbose_name='EAS_activation_ID', db_column='EAS_activation_ID')
    Serial_number = models.TextField(null=True, blank=True, verbose_name='Serial_number', db_column='Serial_number')
    Manufacturer = models.TextField(null=True, blank=True, verbose_name='Manufacturer', db_column='Manufacturer')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    EAS_activated = models.TextField(null=True, blank=True, verbose_name='EAS_activated', db_column='EAS_activated')
    IMEI = models.TextField(null=True, blank=True, verbose_name='IMEI', db_column='IMEI')
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True, verbose_name='Last_EAS_sync_time', db_column='Last_EAS_sync_time')
    EAS_reason = models.TextField(null=True, blank=True, verbose_name='EAS_reason', db_column='EAS_reason')
    EAS_status = models.TextField(null=True, blank=True, verbose_name='EAS_status', db_column='EAS_status')
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True, verbose_name='Compliance_grace_period_expiration', db_column='Compliance_grace_period_expiration')
    Security_patch_level = models.TextField(null=True, blank=True, verbose_name='Security_patch_level', db_column='Security_patch_level')
    WiFi_MAC = models.TextField(null=True, blank=True, verbose_name='WiFi_MAC', db_column='WiFi_MAC')
    MEID = models.TextField(null=True, blank=True, verbose_name='MEID', db_column='MEID')
    Subscriber_carrier = models.TextField(null=True, blank=True, verbose_name='Subscriber_carrier', db_column='Subscriber_carrier')
    Total_storage = models.TextField(null=True, blank=True, verbose_name='Total_storage', db_column='Total_storage')
    Free_storage = models.TextField(null=True, blank=True, verbose_name='Free_storage', db_column='Free_storage')
    Management_name = models.TextField(null=True, blank=True, verbose_name='Management_name', db_column='Management_name')
    Category = models.TextField(null=True, blank=True, verbose_name='Category', db_column='Category')
    UserId = models.TextField(null=True, blank=True, verbose_name='UserId', db_column='UserId')
    Primary_user_UPN = models.TextField(null=True, blank=True, verbose_name='Primary_user_UPN', db_column='Primary_user_UPN')
    Primary_user_email_address = models.TextField(null=True, blank=True, verbose_name='Primary_user_email_address', db_column='Primary_user_email_address')
    Primary_user_display_name = models.TextField(null=True, blank=True, verbose_name='Primary_user_display_name', db_column='Primary_user_display_name')
    WiFiIPv4Address = models.TextField(null=True, blank=True, verbose_name='WiFiIPv4Address', db_column='WiFiIPv4Address')
    WiFiSubnetID = models.TextField(null=True, blank=True, verbose_name='WiFiSubnetID', db_column='WiFiSubnetID')
    Compliance = models.TextField(null=True, blank=True, verbose_name='Compliance', db_column='Compliance')
    Managed_by = models.TextField(null=True, blank=True, verbose_name='Managed_by', db_column='Managed_by')
    Ownership = models.TextField(null=True, blank=True, verbose_name='Ownership', db_column='Ownership')
    Device_state = models.TextField(null=True, blank=True, verbose_name='Device_state', db_column='Device_state')
    Intune_registered = models.TextField(null=True, blank=True, verbose_name='Intune_registered', db_column='Intune_registered')
    Supervised = models.TextField(null=True, blank=True, verbose_name='Supervised', db_column='Supervised')
    Encrypted = models.TextField(null=True, blank=True, verbose_name='Encrypted', db_column='Encrypted')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    SkuFamily = models.TextField(null=True, blank=True, verbose_name='SkuFamily', db_column='SkuFamily')
    JoinType = models.TextField(null=True, blank=True, verbose_name='JoinType', db_column='JoinType')
    Phone_number = models.TextField(null=True, blank=True, verbose_name='Phone_number', db_column='Phone_number')
    Jailbroken = models.TextField(null=True, blank=True, verbose_name='Jailbroken', db_column='Jailbroken')
    ICCID = models.TextField(null=True, blank=True, verbose_name='ICCID', db_column='ICCID')
    EthernetMAC = models.TextField(null=True, blank=True, verbose_name='EthernetMAC', db_column='EthernetMAC')
    CellularTechnology = models.TextField(null=True, blank=True, verbose_name='CellularTechnology', db_column='CellularTechnology')
    ProcessorArchitecture = models.TextField(null=True, blank=True, verbose_name='ProcessorArchitecture', db_column='ProcessorArchitecture')
    EID = models.TextField(null=True, blank=True, verbose_name='EID', db_column='EID')
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True, verbose_name='SystemManagementBIOSVersion', db_column='SystemManagementBIOSVersion')
    TPMManufacturerId = models.TextField(null=True, blank=True, verbose_name='TPMManufacturerId', db_column='TPMManufacturerId')
    TPMManufacturerVersion = models.TextField(null=True, blank=True, verbose_name='TPMManufacturerVersion', db_column='TPMManufacturerVersion')
    ProductName = models.TextField(null=True, blank=True, verbose_name='ProductName', db_column='ProductName')
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True, verbose_name='Management_certificate_expiration_date', db_column='Management_certificate_expiration_date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Enrollment_date', 'Last_checkin', 'Last_EAS_sync_time', 'Compliance_grace_period_expiration', 'Management_certificate_expiration_date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AllDefenderIntunePolicies(models.Model):
    ID = models.AutoField(primary_key=True)
    Policy_name = models.TextField(null=True, blank=True, verbose_name='Policy_name', db_column='Policy_name')
    Policy_category = models.TextField(null=True, blank=True, verbose_name='Policy_category', db_column='Policy_category')
    Assigned = models.TextField(null=True, blank=True, verbose_name='Assigned', db_column='Assigned')
    Platform = models.TextField(null=True, blank=True, verbose_name='Platform', db_column='Platform')
    Target = models.TextField(null=True, blank=True, verbose_name='Target', db_column='Target')
    Last_modified = models.BigIntegerField(null=True, blank=True, verbose_name='Last_modified', db_column='Last_modified')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Last_modified']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Enrollment_date = models.TextField(null=True, blank=True, verbose_name='Enrollment_date', db_column='Enrollment_date')
    Last_checkin = models.TextField(null=True, blank=True, verbose_name='Last_checkin', db_column='Last_checkin')
    Azure_AD_Device_ID = models.TextField(null=True, blank=True, verbose_name='Azure_AD_Device_ID', db_column='Azure_AD_Device_ID')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    Azure_AD_registered = models.TextField(null=True, blank=True, verbose_name='Azure_AD_registered', db_column='Azure_AD_registered')
    EAS_activation_ID = models.TextField(null=True, blank=True, verbose_name='EAS_activation_ID', db_column='EAS_activation_ID')
    Serial_number = models.TextField(null=True, blank=True, verbose_name='Serial_number', db_column='Serial_number')
    Manufacturer = models.TextField(null=True, blank=True, verbose_name='Manufacturer', db_column='Manufacturer')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    EAS_activated = models.TextField(null=True, blank=True, verbose_name='EAS_activated', db_column='EAS_activated')
    IMEI = models.TextField(null=True, blank=True, verbose_name='IMEI', db_column='IMEI')
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True, verbose_name='Last_EAS_sync_time', db_column='Last_EAS_sync_time')
    EAS_reason = models.TextField(null=True, blank=True, verbose_name='EAS_reason', db_column='EAS_reason')
    EAS_status = models.TextField(null=True, blank=True, verbose_name='EAS_status', db_column='EAS_status')
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True, verbose_name='Compliance_grace_period_expiration', db_column='Compliance_grace_period_expiration')
    Security_patch_level = models.TextField(null=True, blank=True, verbose_name='Security_patch_level', db_column='Security_patch_level')
    WiFi_MAC = models.TextField(null=True, blank=True, verbose_name='WiFi_MAC', db_column='WiFi_MAC')
    MEID = models.TextField(null=True, blank=True, verbose_name='MEID', db_column='MEID')
    Subscriber_carrier = models.TextField(null=True, blank=True, verbose_name='Subscriber_carrier', db_column='Subscriber_carrier')
    Total_storage = models.TextField(null=True, blank=True, verbose_name='Total_storage', db_column='Total_storage')
    Free_storage = models.TextField(null=True, blank=True, verbose_name='Free_storage', db_column='Free_storage')
    Management_name = models.TextField(null=True, blank=True, verbose_name='Management_name', db_column='Management_name')
    Category = models.TextField(null=True, blank=True, verbose_name='Category', db_column='Category')
    UserId = models.TextField(null=True, blank=True, verbose_name='UserId', db_column='UserId')
    Primary_user_UPN = models.TextField(null=True, blank=True, verbose_name='Primary_user_UPN', db_column='Primary_user_UPN')
    Primary_user_email_address = models.TextField(null=True, blank=True, verbose_name='Primary_user_email_address', db_column='Primary_user_email_address')
    Primary_user_display_name = models.TextField(null=True, blank=True, verbose_name='Primary_user_display_name', db_column='Primary_user_display_name')
    WiFiIPv4Address = models.TextField(null=True, blank=True, verbose_name='WiFiIPv4Address', db_column='WiFiIPv4Address')
    WiFiSubnetID = models.TextField(null=True, blank=True, verbose_name='WiFiSubnetID', db_column='WiFiSubnetID')
    Compliance = models.TextField(null=True, blank=True, verbose_name='Compliance', db_column='Compliance')
    Managed_by = models.TextField(null=True, blank=True, verbose_name='Managed_by', db_column='Managed_by')
    Ownership = models.TextField(null=True, blank=True, verbose_name='Ownership', db_column='Ownership')
    Device_state = models.TextField(null=True, blank=True, verbose_name='Device_state', db_column='Device_state')
    Intune_registered = models.TextField(null=True, blank=True, verbose_name='Intune_registered', db_column='Intune_registered')
    Supervised = models.TextField(null=True, blank=True, verbose_name='Supervised', db_column='Supervised')
    Encrypted = models.TextField(null=True, blank=True, verbose_name='Encrypted', db_column='Encrypted')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    SkuFamily = models.TextField(null=True, blank=True, verbose_name='SkuFamily', db_column='SkuFamily')
    JoinType = models.TextField(null=True, blank=True, verbose_name='JoinType', db_column='JoinType')
    Phone_number = models.TextField(null=True, blank=True, verbose_name='Phone_number', db_column='Phone_number')
    Jailbroken = models.TextField(null=True, blank=True, verbose_name='Jailbroken', db_column='Jailbroken')
    ICCID = models.TextField(null=True, blank=True, verbose_name='ICCID', db_column='ICCID')
    EthernetMAC = models.TextField(null=True, blank=True, verbose_name='EthernetMAC', db_column='EthernetMAC')
    CellularTechnology = models.TextField(null=True, blank=True, verbose_name='CellularTechnology', db_column='CellularTechnology')
    ProcessorArchitecture = models.TextField(null=True, blank=True, verbose_name='ProcessorArchitecture', db_column='ProcessorArchitecture')
    EID = models.TextField(null=True, blank=True, verbose_name='EID', db_column='EID')
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True, verbose_name='SystemManagementBIOSVersion', db_column='SystemManagementBIOSVersion')
    TPMManufacturerId = models.TextField(null=True, blank=True, verbose_name='TPMManufacturerId', db_column='TPMManufacturerId')
    TPMManufacturerVersion = models.TextField(null=True, blank=True, verbose_name='TPMManufacturerVersion', db_column='TPMManufacturerVersion')
    ProductName = models.TextField(null=True, blank=True, verbose_name='ProductName', db_column='ProductName')
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True, verbose_name='Management_certificate_expiration_date', db_column='Management_certificate_expiration_date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Last_EAS_sync_time', 'Compliance_grace_period_expiration', 'Management_certificate_expiration_date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSAVStatus(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Device_group = models.TextField(null=True, blank=True, verbose_name='Device_group', db_column='Device_group')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    OS_platform = models.TextField(null=True, blank=True, verbose_name='OS_platform', db_column='OS_platform')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    AV_mode = models.TextField(null=True, blank=True, verbose_name='AV_mode', db_column='AV_mode')
    Security_intel_version = models.TextField(null=True, blank=True, verbose_name='Security_intel_version', db_column='Security_intel_version')
    Engine_version = models.TextField(null=True, blank=True, verbose_name='Engine_version', db_column='Engine_version')
    Platform_version = models.TextField(null=True, blank=True, verbose_name='Platform_version', db_column='Platform_version')
    Quick_scan_status = models.TextField(null=True, blank=True, verbose_name='Quick_scan_status', db_column='Quick_scan_status')
    Quick_scan_error = models.TextField(null=True, blank=True, verbose_name='Quick_scan_error', db_column='Quick_scan_error')
    Full_scan_status = models.TextField(null=True, blank=True, verbose_name='Full_scan_status', db_column='Full_scan_status')
    Full_scan_error = models.TextField(null=True, blank=True, verbose_name='Full_scan_error', db_column='Full_scan_error')
    Quick_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Quick_scan_time', db_column='Quick_scan_time')
    Full_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Full_scan_time', db_column='Full_scan_time')
    Last_seen = models.BigIntegerField(null=True, blank=True, verbose_name='Last_seen', db_column='Last_seen')
    Data_refresh_timestamp = models.BigIntegerField(null=True, blank=True, verbose_name='Data_refresh_timestamp', db_column='Data_refresh_timestamp')
    Engine_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Engine_update_time', db_column='Engine_update_time')
    Signature_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_update_time', db_column='Signature_update_time')
    Platform_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Platform_update_time', db_column='Platform_update_time')
    Security_intelligence_up_to_date = models.TextField(null=True, blank=True, verbose_name='Security_intelligence_up_to_date', db_column='Security_intelligence_up_to_date')
    Engine_up_to_date = models.TextField(null=True, blank=True, verbose_name='Engine_up_to_date', db_column='Engine_up_to_date')
    Platform_up_to_date = models.TextField(null=True, blank=True, verbose_name='Platform_up_to_date', db_column='Platform_up_to_date')
    Security_intel_publish_time = models.BigIntegerField(null=True, blank=True, verbose_name='Security_intel_publish_time', db_column='Security_intel_publish_time')
    Signature_refresh_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_refresh_time', db_column='Signature_refresh_time')
    eBPF_status = models.TextField(null=True, blank=True, verbose_name='eBPF_status', db_column='eBPF_status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Quick_scan_time', 'Full_scan_time', 'Last_seen', 'Data_refresh_timestamp', 'Engine_update_time', 'Signature_update_time', 'Platform_update_time', 'Security_intel_publish_time', 'Signature_refresh_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTAVStatus(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Device_group = models.TextField(null=True, blank=True, verbose_name='Device_group', db_column='Device_group')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    OS_platform = models.TextField(null=True, blank=True, verbose_name='OS_platform', db_column='OS_platform')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    AV_mode = models.TextField(null=True, blank=True, verbose_name='AV_mode', db_column='AV_mode')
    Security_intel_version = models.TextField(null=True, blank=True, verbose_name='Security_intel_version', db_column='Security_intel_version')
    Engine_version = models.TextField(null=True, blank=True, verbose_name='Engine_version', db_column='Engine_version')
    Platform_version = models.TextField(null=True, blank=True, verbose_name='Platform_version', db_column='Platform_version')
    Quick_scan_status = models.TextField(null=True, blank=True, verbose_name='Quick_scan_status', db_column='Quick_scan_status')
    Quick_scan_error = models.TextField(null=True, blank=True, verbose_name='Quick_scan_error', db_column='Quick_scan_error')
    Full_scan_status = models.TextField(null=True, blank=True, verbose_name='Full_scan_status', db_column='Full_scan_status')
    Full_scan_error = models.TextField(null=True, blank=True, verbose_name='Full_scan_error', db_column='Full_scan_error')
    Quick_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Quick_scan_time', db_column='Quick_scan_time')
    Full_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Full_scan_time', db_column='Full_scan_time')
    Last_seen = models.BigIntegerField(null=True, blank=True, verbose_name='Last_seen', db_column='Last_seen')
    Data_refresh_timestamp = models.BigIntegerField(null=True, blank=True, verbose_name='Data_refresh_timestamp', db_column='Data_refresh_timestamp')
    Engine_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Engine_update_time', db_column='Engine_update_time')
    Signature_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_update_time', db_column='Signature_update_time')
    Platform_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Platform_update_time', db_column='Platform_update_time')
    Security_intelligence_up_to_date = models.TextField(null=True, blank=True, verbose_name='Security_intelligence_up_to_date', db_column='Security_intelligence_up_to_date')
    Engine_up_to_date = models.TextField(null=True, blank=True, verbose_name='Engine_up_to_date', db_column='Engine_up_to_date')
    Platform_up_to_date = models.TextField(null=True, blank=True, verbose_name='Platform_up_to_date', db_column='Platform_up_to_date')
    Security_intel_publish_time = models.BigIntegerField(null=True, blank=True, verbose_name='Security_intel_publish_time', db_column='Security_intel_publish_time')
    Signature_refresh_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_refresh_time', db_column='Signature_refresh_time')
    eBPF_status = models.TextField(null=True, blank=True, verbose_name='eBPF_status', db_column='eBPF_status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Quick_scan_time', 'Full_scan_time', 'Last_seen', 'Data_refresh_timestamp', 'Engine_update_time', 'Signature_update_time', 'Platform_update_time', 'Security_intel_publish_time', 'Signature_refresh_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ASECAVStatus(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Device_group = models.TextField(null=True, blank=True, verbose_name='Device_group', db_column='Device_group')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    OS_platform = models.TextField(null=True, blank=True, verbose_name='OS_platform', db_column='OS_platform')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    AV_mode = models.TextField(null=True, blank=True, verbose_name='AV_mode', db_column='AV_mode')
    Security_intel_version = models.TextField(null=True, blank=True, verbose_name='Security_intel_version', db_column='Security_intel_version')
    Engine_version = models.TextField(null=True, blank=True, verbose_name='Engine_version', db_column='Engine_version')
    Platform_version = models.TextField(null=True, blank=True, verbose_name='Platform_version', db_column='Platform_version')
    Quick_scan_status = models.TextField(null=True, blank=True, verbose_name='Quick_scan_status', db_column='Quick_scan_status')
    Quick_scan_error = models.TextField(null=True, blank=True, verbose_name='Quick_scan_error', db_column='Quick_scan_error')
    Full_scan_status = models.TextField(null=True, blank=True, verbose_name='Full_scan_status', db_column='Full_scan_status')
    Full_scan_error = models.TextField(null=True, blank=True, verbose_name='Full_scan_error', db_column='Full_scan_error')
    Quick_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Quick_scan_time', db_column='Quick_scan_time')
    Full_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Full_scan_time', db_column='Full_scan_time')
    Last_seen = models.BigIntegerField(null=True, blank=True, verbose_name='Last_seen', db_column='Last_seen')
    Data_refresh_timestamp = models.BigIntegerField(null=True, blank=True, verbose_name='Data_refresh_timestamp', db_column='Data_refresh_timestamp')
    Engine_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Engine_update_time', db_column='Engine_update_time')
    Signature_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_update_time', db_column='Signature_update_time')
    Platform_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Platform_update_time', db_column='Platform_update_time')
    Security_intelligence_up_to_date = models.TextField(null=True, blank=True, verbose_name='Security_intelligence_up_to_date', db_column='Security_intelligence_up_to_date')
    Engine_up_to_date = models.TextField(null=True, blank=True, verbose_name='Engine_up_to_date', db_column='Engine_up_to_date')
    Platform_up_to_date = models.TextField(null=True, blank=True, verbose_name='Platform_up_to_date', db_column='Platform_up_to_date')
    Security_intel_publish_time = models.BigIntegerField(null=True, blank=True, verbose_name='Security_intel_publish_time', db_column='Security_intel_publish_time')
    Signature_refresh_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_refresh_time', db_column='Signature_refresh_time')
    eBPF_status = models.TextField(null=True, blank=True, verbose_name='eBPF_status', db_column='eBPF_status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Quick_scan_time', 'Full_scan_time', 'Last_seen', 'Data_refresh_timestamp', 'Engine_update_time', 'Signature_update_time', 'Platform_update_time', 'Security_intel_publish_time', 'Signature_refresh_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class NupayAVStatus(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    Device_group = models.TextField(null=True, blank=True, verbose_name='Device_group', db_column='Device_group')
    OS = models.TextField(null=True, blank=True, verbose_name='OS', db_column='OS')
    OS_platform = models.TextField(null=True, blank=True, verbose_name='OS_platform', db_column='OS_platform')
    OS_version = models.TextField(null=True, blank=True, verbose_name='OS_version', db_column='OS_version')
    AV_mode = models.TextField(null=True, blank=True, verbose_name='AV_mode', db_column='AV_mode')
    Security_intel_version = models.TextField(null=True, blank=True, verbose_name='Security_intel_version', db_column='Security_intel_version')
    Engine_version = models.TextField(null=True, blank=True, verbose_name='Engine_version', db_column='Engine_version')
    Platform_version = models.TextField(null=True, blank=True, verbose_name='Platform_version', db_column='Platform_version')
    Quick_scan_status = models.TextField(null=True, blank=True, verbose_name='Quick_scan_status', db_column='Quick_scan_status')
    Quick_scan_error = models.TextField(null=True, blank=True, verbose_name='Quick_scan_error', db_column='Quick_scan_error')
    Full_scan_status = models.TextField(null=True, blank=True, verbose_name='Full_scan_status', db_column='Full_scan_status')
    Full_scan_error = models.TextField(null=True, blank=True, verbose_name='Full_scan_error', db_column='Full_scan_error')
    Quick_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Quick_scan_time', db_column='Quick_scan_time')
    Full_scan_time = models.BigIntegerField(null=True, blank=True, verbose_name='Full_scan_time', db_column='Full_scan_time')
    Last_seen = models.BigIntegerField(null=True, blank=True, verbose_name='Last_seen', db_column='Last_seen')
    Data_refresh_timestamp = models.BigIntegerField(null=True, blank=True, verbose_name='Data_refresh_timestamp', db_column='Data_refresh_timestamp')
    Engine_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Engine_update_time', db_column='Engine_update_time')
    Signature_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_update_time', db_column='Signature_update_time')
    Platform_update_time = models.BigIntegerField(null=True, blank=True, verbose_name='Platform_update_time', db_column='Platform_update_time')
    Security_intelligence_up_to_date = models.TextField(null=True, blank=True, verbose_name='Security_intelligence_up_to_date', db_column='Security_intelligence_up_to_date')
    Engine_up_to_date = models.TextField(null=True, blank=True, verbose_name='Engine_up_to_date', db_column='Engine_up_to_date')
    Platform_up_to_date = models.TextField(null=True, blank=True, verbose_name='Platform_up_to_date', db_column='Platform_up_to_date')
    Security_intel_publish_time = models.BigIntegerField(null=True, blank=True, verbose_name='Security_intel_publish_time', db_column='Security_intel_publish_time')
    Signature_refresh_time = models.BigIntegerField(null=True, blank=True, verbose_name='Signature_refresh_time', db_column='Signature_refresh_time')
    eBPF_status = models.TextField(null=True, blank=True, verbose_name='eBPF_status', db_column='eBPF_status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Quick_scan_time', 'Full_scan_time', 'Last_seen', 'Data_refresh_timestamp', 'Engine_update_time', 'Signature_update_time', 'Platform_update_time', 'Security_intel_publish_time', 'Signature_refresh_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AltronHealthTechUsersDetailed(models.Model):
    ID = models.AutoField(primary_key=True)
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    AccountName = models.TextField(null=True, blank=True, verbose_name='AccountName', db_column='AccountName')
    DisplayName = models.TextField(null=True, blank=True, verbose_name='DisplayName', db_column='DisplayName')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    WhenCreated = models.BigIntegerField(null=True, blank=True, verbose_name='WhenCreated', db_column='WhenCreated')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    PasswordLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='PasswordLastSet', db_column='PasswordLastSet')
    ElevatedRole = models.TextField(null=True, blank=True, verbose_name='ElevatedRole', db_column='ElevatedRole')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['WhenCreated', 'LastLogonDate', 'PasswordLastSet']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaADvsTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Termination_Date = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_AccountName = models.TextField(null=True, blank=True)
    d_DisplayName = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_WhenCreated = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_PasswordLastSet = models.BigIntegerField(null=True, blank=True)
    d_ElevatedRole = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 12  # Do not change this value
    date_fields_to_convert = ['d_LastLogonDate', 'd_PasswordLastSet', 'Termination_Date', 'd_WhenCreated']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaNetsuiteActiveInactivevsAD(models.Model):
    ID = models.AutoField(primary_key=True)
    Username = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    Role = models.TextField(null=True, blank=True)
    Inactive = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_AccountName = models.TextField(null=True, blank=True)
    d_DisplayName = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_WhenCreated = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_PasswordLastSet = models.BigIntegerField(null=True, blank=True)
    d_ElevatedRole = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 13  # Do not change this value
    date_fields_to_convert = ['d_LastLogonDate', 'd_WhenCreated', 'd_PasswordLastSet']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaAHTHelpdeskticketstoHR(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_First_Name = models.TextField(null=True, blank=True)
    Employee_Surname = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Termination_Date = models.BigIntegerField(null=True, blank=True)
    Business_Title = models.TextField(null=True, blank=True)
    Reports_To = models.TextField(null=True, blank=True)
    d_Activities = models.TextField(null=True, blank=True)
    d_Status = models.TextField(null=True, blank=True)
    d_Assigned_to = models.TextField(null=True, blank=True)
    d_Close_date = models.BigIntegerField(null=True, blank=True)
    d_Created_on = models.BigIntegerField(null=True, blank=True)
    d_Customer = models.TextField(null=True, blank=True)
    d_Helpdesk_Team = models.TextField(null=True, blank=True)
    d_Kanban_State = models.TextField(null=True, blank=True)
    d_Last_Updated_on = models.BigIntegerField(null=True, blank=True)
    d_Originator_Email = models.TextField(null=True, blank=True)
    d_Priority = models.TextField(null=True, blank=True)
    d_Stage = models.TextField(null=True, blank=True)
    d_Subject = models.TextField(null=True, blank=True)
    d_Ticket_IDs_Sequence = models.IntegerField(null=True, blank=True)
    d_Ticket_Type = models.TextField(null=True, blank=True)
    d_Time_Spent = models.FloatField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 14  # Do not change this value
    date_fields_to_convert = ['Termination_Date', 'd_Created_on', 'd_Close_date', 'd_Last_Updated_on']
    integer_fields = ['d_Ticket_IDs_Sequence']
    float_fields = ['d_Time_Spent']
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AltronHealthTechUsersDetailed2(models.Model):
    ID = models.AutoField(primary_key=True)
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    AccountName = models.TextField(null=True, blank=True, verbose_name='AccountName', db_column='AccountName')
    DisplayName = models.TextField(null=True, blank=True, verbose_name='DisplayName', db_column='DisplayName')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    WhenCreated = models.BigIntegerField(null=True, blank=True, verbose_name='WhenCreated', db_column='WhenCreated')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    PasswordLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='PasswordLastSet', db_column='PasswordLastSet')
    ElevatedRole = models.TextField(null=True, blank=True, verbose_name='ElevatedRole', db_column='ElevatedRole')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['WhenCreated', 'LastLogonDate', 'PasswordLastSet']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADUsers1VsADUsers2(models.Model):
    ID = models.AutoField(primary_key=True)
    SamAccountName = models.TextField(null=True, blank=True)
    Username = models.TextField(null=True, blank=True)
    AccountName = models.TextField(null=True, blank=True)
    DisplayName = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    WhenCreated = models.BigIntegerField(null=True, blank=True)
    LastLogonDate = models.BigIntegerField(null=True, blank=True)
    Enabled = models.TextField(null=True, blank=True)
    PasswordLastSet = models.BigIntegerField(null=True, blank=True)
    ElevatedRole = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_AccountName = models.TextField(null=True, blank=True)
    d_DisplayName = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_Email = models.TextField(null=True, blank=True)
    d_WhenCreated = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_PasswordLastSet = models.BigIntegerField(null=True, blank=True)
    d_ElevatedRole = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 15  # Do not change this value
    date_fields_to_convert = ['d_LastLogonDate', 'WhenCreated', 'LastLogonDate', 'd_WhenCreated', 'PasswordLastSet', 'd_PasswordLastSet']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaAD2vsTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    SamAccountName = models.TextField(null=True, blank=True)
    Username = models.TextField(null=True, blank=True)
    AccountName = models.TextField(null=True, blank=True)
    DisplayName = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    WhenCreated = models.BigIntegerField(null=True, blank=True)
    LastLogonDate = models.BigIntegerField(null=True, blank=True)
    Enabled = models.TextField(null=True, blank=True)
    PasswordLastSet = models.BigIntegerField(null=True, blank=True)
    ElevatedRole = models.TextField(null=True, blank=True)
    d_Employee_First_Name = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)
    d_Business_Title = models.TextField(null=True, blank=True)
    d_Reports_To = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 16  # Do not change this value
    date_fields_to_convert = ['d_Termination_Date', 'PasswordLastSet', 'WhenCreated', 'LastLogonDate']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaIntunevsAV(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Enrollment_date = models.TextField(null=True, blank=True)
    Last_checkin = models.TextField(null=True, blank=True)
    Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Azure_AD_registered = models.TextField(null=True, blank=True)
    EAS_activation_ID = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    EAS_activated = models.TextField(null=True, blank=True)
    IMEI = models.TextField(null=True, blank=True)
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    EAS_reason = models.TextField(null=True, blank=True)
    EAS_status = models.TextField(null=True, blank=True)
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    Security_patch_level = models.TextField(null=True, blank=True)
    WiFi_MAC = models.TextField(null=True, blank=True)
    MEID = models.TextField(null=True, blank=True)
    Subscriber_carrier = models.TextField(null=True, blank=True)
    Total_storage = models.TextField(null=True, blank=True)
    Free_storage = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    UserId = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_display_name = models.TextField(null=True, blank=True)
    WiFiIPv4Address = models.TextField(null=True, blank=True)
    WiFiSubnetID = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Intune_registered = models.TextField(null=True, blank=True)
    Supervised = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    SkuFamily = models.TextField(null=True, blank=True)
    JoinType = models.TextField(null=True, blank=True)
    Phone_number = models.TextField(null=True, blank=True)
    Jailbroken = models.TextField(null=True, blank=True)
    ICCID = models.TextField(null=True, blank=True)
    EthernetMAC = models.TextField(null=True, blank=True)
    CellularTechnology = models.TextField(null=True, blank=True)
    ProcessorArchitecture = models.TextField(null=True, blank=True)
    EID = models.TextField(null=True, blank=True)
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    TPMManufacturerId = models.TextField(null=True, blank=True)
    TPMManufacturerVersion = models.TextField(null=True, blank=True)
    ProductName = models.TextField(null=True, blank=True)
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)
    d_DeviceName = models.TextField(null=True, blank=True)
    d_UPN = models.TextField(null=True, blank=True)
    d_ReportStatus = models.TextField(null=True, blank=True)
    d_ReportStatus_loc = models.TextField(null=True, blank=True)
    d_AssignmentFilterIds = models.TextField(null=True, blank=True)
    d_PspdpuLastModifiedTimeUtc = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 17  # Do not change this value
    date_fields_to_convert = ['d_PspdpuLastModifiedTimeUtc', 'Compliance_grace_period_expiration', 'Management_certificate_expiration_date', 'Last_EAS_sync_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AHTIntunevsDefender(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Enrollment_date = models.TextField(null=True, blank=True)
    Last_checkin = models.TextField(null=True, blank=True)
    Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Azure_AD_registered = models.TextField(null=True, blank=True)
    EAS_activation_ID = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    EAS_activated = models.TextField(null=True, blank=True)
    IMEI = models.TextField(null=True, blank=True)
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    EAS_reason = models.TextField(null=True, blank=True)
    EAS_status = models.TextField(null=True, blank=True)
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    Security_patch_level = models.TextField(null=True, blank=True)
    WiFi_MAC = models.TextField(null=True, blank=True)
    MEID = models.TextField(null=True, blank=True)
    Subscriber_carrier = models.TextField(null=True, blank=True)
    Total_storage = models.TextField(null=True, blank=True)
    Free_storage = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    UserId = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_display_name = models.TextField(null=True, blank=True)
    WiFiIPv4Address = models.TextField(null=True, blank=True)
    WiFiSubnetID = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Intune_registered = models.TextField(null=True, blank=True)
    Supervised = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    SkuFamily = models.TextField(null=True, blank=True)
    JoinType = models.TextField(null=True, blank=True)
    Phone_number = models.TextField(null=True, blank=True)
    Jailbroken = models.TextField(null=True, blank=True)
    ICCID = models.TextField(null=True, blank=True)
    EthernetMAC = models.TextField(null=True, blank=True)
    CellularTechnology = models.TextField(null=True, blank=True)
    ProcessorArchitecture = models.TextField(null=True, blank=True)
    EID = models.TextField(null=True, blank=True)
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    TPMManufacturerId = models.TextField(null=True, blank=True)
    TPMManufacturerVersion = models.TextField(null=True, blank=True)
    ProductName = models.TextField(null=True, blank=True)
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_Name = models.TextField(null=True, blank=True)
    d_Device_Category = models.TextField(null=True, blank=True)
    d_Device_Type = models.TextField(null=True, blank=True)
    d_Device_Subtype = models.TextField(null=True, blank=True)
    d_Discovery_sources = models.TextField(null=True, blank=True)
    d_Domain = models.TextField(null=True, blank=True)
    d_AAD_Device_Id = models.TextField(null=True, blank=True)
    d_First_Seen = models.BigIntegerField(null=True, blank=True)
    d_Last_device_update = models.BigIntegerField(null=True, blank=True)
    d_OS_Platform = models.TextField(null=True, blank=True)
    d_OS_Distribution = models.TextField(null=True, blank=True)
    d_OS_Version = models.TextField(null=True, blank=True)
    d_OS_Build = models.TextField(null=True, blank=True)
    d_Windows_10_Version = models.TextField(null=True, blank=True)
    d_Tags = models.TextField(null=True, blank=True)
    d_Group = models.TextField(null=True, blank=True)
    d_Is_AAD_Joined = models.TextField(null=True, blank=True)
    d_Device_IPs = models.TextField(null=True, blank=True)
    d_Device_MACs = models.TextField(null=True, blank=True)
    d_Risk_Level = models.TextField(null=True, blank=True)
    d_Exposure_Level = models.TextField(null=True, blank=True)
    d_Health_Status = models.TextField(null=True, blank=True)
    d_Onboarding_Status = models.TextField(null=True, blank=True)
    d_Device_Role = models.TextField(null=True, blank=True)
    d_Cloud_Platforms = models.TextField(null=True, blank=True)
    d_Is_Internet_Facing = models.TextField(null=True, blank=True)
    d_Enrollment_Status_Code = models.TextField(null=True, blank=True)
    d_Managed_By = models.TextField(null=True, blank=True)
    d_Enrollment_Status = models.TextField(null=True, blank=True)
    d_Vendor = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_Firmware_versions = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 18  # Do not change this value
    date_fields_to_convert = ['Last_EAS_sync_time', 'Management_certificate_expiration_date', 'd_First_Seen', 'Compliance_grace_period_expiration', 'd_Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaAHTIntunevsDefender2(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Enrollment_date = models.TextField(null=True, blank=True)
    Last_checkin = models.TextField(null=True, blank=True)
    Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Azure_AD_registered = models.TextField(null=True, blank=True)
    EAS_activation_ID = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    EAS_activated = models.TextField(null=True, blank=True)
    IMEI = models.TextField(null=True, blank=True)
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    EAS_reason = models.TextField(null=True, blank=True)
    EAS_status = models.TextField(null=True, blank=True)
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    Security_patch_level = models.TextField(null=True, blank=True)
    WiFi_MAC = models.TextField(null=True, blank=True)
    MEID = models.TextField(null=True, blank=True)
    Subscriber_carrier = models.TextField(null=True, blank=True)
    Total_storage = models.TextField(null=True, blank=True)
    Free_storage = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    UserId = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_display_name = models.TextField(null=True, blank=True)
    WiFiIPv4Address = models.TextField(null=True, blank=True)
    WiFiSubnetID = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Intune_registered = models.TextField(null=True, blank=True)
    Supervised = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    SkuFamily = models.TextField(null=True, blank=True)
    JoinType = models.TextField(null=True, blank=True)
    Phone_number = models.TextField(null=True, blank=True)
    Jailbroken = models.TextField(null=True, blank=True)
    ICCID = models.TextField(null=True, blank=True)
    EthernetMAC = models.TextField(null=True, blank=True)
    CellularTechnology = models.TextField(null=True, blank=True)
    ProcessorArchitecture = models.TextField(null=True, blank=True)
    EID = models.TextField(null=True, blank=True)
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    TPMManufacturerId = models.TextField(null=True, blank=True)
    TPMManufacturerVersion = models.TextField(null=True, blank=True)
    ProductName = models.TextField(null=True, blank=True)
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_Name = models.TextField(null=True, blank=True)
    d_Device_Category = models.TextField(null=True, blank=True)
    d_Device_Type = models.TextField(null=True, blank=True)
    d_Device_Subtype = models.TextField(null=True, blank=True)
    d_Discovery_sources = models.TextField(null=True, blank=True)
    d_Domain = models.TextField(null=True, blank=True)
    d_AAD_Device_Id = models.TextField(null=True, blank=True)
    d_First_Seen = models.BigIntegerField(null=True, blank=True)
    d_Last_device_update = models.BigIntegerField(null=True, blank=True)
    d_OS_Platform = models.TextField(null=True, blank=True)
    d_OS_Distribution = models.TextField(null=True, blank=True)
    d_OS_Version = models.TextField(null=True, blank=True)
    d_OS_Build = models.TextField(null=True, blank=True)
    d_Windows_10_Version = models.TextField(null=True, blank=True)
    d_Tags = models.TextField(null=True, blank=True)
    d_Group = models.TextField(null=True, blank=True)
    d_Is_AAD_Joined = models.TextField(null=True, blank=True)
    d_Device_IPs = models.TextField(null=True, blank=True)
    d_Device_MACs = models.TextField(null=True, blank=True)
    d_Risk_Level = models.TextField(null=True, blank=True)
    d_Exposure_Level = models.TextField(null=True, blank=True)
    d_Health_Status = models.TextField(null=True, blank=True)
    d_Onboarding_Status = models.TextField(null=True, blank=True)
    d_Device_Role = models.TextField(null=True, blank=True)
    d_Cloud_Platforms = models.TextField(null=True, blank=True)
    d_Is_Internet_Facing = models.TextField(null=True, blank=True)
    d_Enrollment_Status_Code = models.TextField(null=True, blank=True)
    d_Managed_By = models.TextField(null=True, blank=True)
    d_Enrollment_Status = models.TextField(null=True, blank=True)
    d_Vendor = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_Firmware_versions = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 19  # Do not change this value
    date_fields_to_convert = ['Last_EAS_sync_time', 'Compliance_grace_period_expiration', 'd_Last_device_update', 'Management_certificate_expiration_date', 'd_First_Seen']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaDefendervsIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_Name = models.TextField(null=True, blank=True)
    Device_Category = models.TextField(null=True, blank=True)
    Device_Type = models.TextField(null=True, blank=True)
    Device_Subtype = models.TextField(null=True, blank=True)
    Discovery_sources = models.TextField(null=True, blank=True)
    Domain = models.TextField(null=True, blank=True)
    AAD_Device_Id = models.TextField(null=True, blank=True)
    First_Seen = models.BigIntegerField(null=True, blank=True)
    Last_device_update = models.BigIntegerField(null=True, blank=True)
    OS_Platform = models.TextField(null=True, blank=True)
    OS_Distribution = models.TextField(null=True, blank=True)
    OS_Version = models.TextField(null=True, blank=True)
    OS_Build = models.TextField(null=True, blank=True)
    Windows_10_Version = models.TextField(null=True, blank=True)
    Tags = models.TextField(null=True, blank=True)
    Group = models.TextField(null=True, blank=True)
    Is_AAD_Joined = models.TextField(null=True, blank=True)
    Device_IPs = models.TextField(null=True, blank=True)
    Device_MACs = models.TextField(null=True, blank=True)
    Risk_Level = models.TextField(null=True, blank=True)
    Exposure_Level = models.TextField(null=True, blank=True)
    Health_Status = models.TextField(null=True, blank=True)
    Onboarding_Status = models.TextField(null=True, blank=True)
    Device_Role = models.TextField(null=True, blank=True)
    Cloud_Platforms = models.TextField(null=True, blank=True)
    Is_Internet_Facing = models.TextField(null=True, blank=True)
    Enrollment_Status_Code = models.TextField(null=True, blank=True)
    Managed_By = models.TextField(null=True, blank=True)
    Enrollment_Status = models.TextField(null=True, blank=True)
    Vendor = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Firmware_versions = models.TextField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_name = models.TextField(null=True, blank=True)
    d_Enrollment_date = models.TextField(null=True, blank=True)
    d_Last_checkin = models.TextField(null=True, blank=True)
    d_Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    d_OS_version = models.TextField(null=True, blank=True)
    d_Azure_AD_registered = models.TextField(null=True, blank=True)
    d_EAS_activation_ID = models.TextField(null=True, blank=True)
    d_Serial_number = models.TextField(null=True, blank=True)
    d_Manufacturer = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_EAS_activated = models.TextField(null=True, blank=True)
    d_IMEI = models.TextField(null=True, blank=True)
    d_Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    d_EAS_reason = models.TextField(null=True, blank=True)
    d_EAS_status = models.TextField(null=True, blank=True)
    d_Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    d_Security_patch_level = models.TextField(null=True, blank=True)
    d_WiFi_MAC = models.TextField(null=True, blank=True)
    d_MEID = models.TextField(null=True, blank=True)
    d_Subscriber_carrier = models.TextField(null=True, blank=True)
    d_Total_storage = models.TextField(null=True, blank=True)
    d_Free_storage = models.TextField(null=True, blank=True)
    d_Management_name = models.TextField(null=True, blank=True)
    d_Category = models.TextField(null=True, blank=True)
    d_UserId = models.TextField(null=True, blank=True)
    d_Primary_user_UPN = models.TextField(null=True, blank=True)
    d_Primary_user_email_address = models.TextField(null=True, blank=True)
    d_Primary_user_display_name = models.TextField(null=True, blank=True)
    d_WiFiIPv4Address = models.TextField(null=True, blank=True)
    d_WiFiSubnetID = models.TextField(null=True, blank=True)
    d_Compliance = models.TextField(null=True, blank=True)
    d_Managed_by = models.TextField(null=True, blank=True)
    d_Ownership = models.TextField(null=True, blank=True)
    d_Device_state = models.TextField(null=True, blank=True)
    d_Intune_registered = models.TextField(null=True, blank=True)
    d_Supervised = models.TextField(null=True, blank=True)
    d_Encrypted = models.TextField(null=True, blank=True)
    d_OS = models.TextField(null=True, blank=True)
    d_SkuFamily = models.TextField(null=True, blank=True)
    d_JoinType = models.TextField(null=True, blank=True)
    d_Phone_number = models.TextField(null=True, blank=True)
    d_Jailbroken = models.TextField(null=True, blank=True)
    d_ICCID = models.TextField(null=True, blank=True)
    d_EthernetMAC = models.TextField(null=True, blank=True)
    d_CellularTechnology = models.TextField(null=True, blank=True)
    d_ProcessorArchitecture = models.TextField(null=True, blank=True)
    d_EID = models.TextField(null=True, blank=True)
    d_SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    d_TPMManufacturerId = models.TextField(null=True, blank=True)
    d_TPMManufacturerVersion = models.TextField(null=True, blank=True)
    d_ProductName = models.TextField(null=True, blank=True)
    d_Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 20  # Do not change this value
    date_fields_to_convert = ['d_Compliance_grace_period_expiration', 'First_Seen', 'd_Management_certificate_expiration_date', 'Last_device_update', 'd_Last_EAS_sync_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaDefendervsIntune2(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_Category = models.TextField(null=True, blank=True)
    Device_Type = models.TextField(null=True, blank=True)
    Device_Subtype = models.TextField(null=True, blank=True)
    Discovery_sources = models.TextField(null=True, blank=True)
    Domain = models.TextField(null=True, blank=True)
    AAD_Device_Id = models.TextField(null=True, blank=True)
    First_Seen = models.BigIntegerField(null=True, blank=True)
    Last_device_update = models.BigIntegerField(null=True, blank=True)
    OS_Platform = models.TextField(null=True, blank=True)
    OS_Distribution = models.TextField(null=True, blank=True)
    OS_Version = models.TextField(null=True, blank=True)
    OS_Build = models.TextField(null=True, blank=True)
    Windows_10_Version = models.TextField(null=True, blank=True)
    Tags = models.TextField(null=True, blank=True)
    Group = models.TextField(null=True, blank=True)
    Is_AAD_Joined = models.TextField(null=True, blank=True)
    Device_IPs = models.TextField(null=True, blank=True)
    Device_MACs = models.TextField(null=True, blank=True)
    Risk_Level = models.TextField(null=True, blank=True)
    Exposure_Level = models.TextField(null=True, blank=True)
    Health_Status = models.TextField(null=True, blank=True)
    Onboarding_Status = models.TextField(null=True, blank=True)
    Device_Role = models.TextField(null=True, blank=True)
    Cloud_Platforms = models.TextField(null=True, blank=True)
    Is_Internet_Facing = models.TextField(null=True, blank=True)
    Enrollment_Status_Code = models.TextField(null=True, blank=True)
    Managed_By = models.TextField(null=True, blank=True)
    Enrollment_Status = models.TextField(null=True, blank=True)
    Vendor = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Firmware_versions = models.TextField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_name = models.TextField(null=True, blank=True)
    d_Enrollment_date = models.TextField(null=True, blank=True)
    d_Last_checkin = models.TextField(null=True, blank=True)
    d_Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    d_OS_version = models.TextField(null=True, blank=True)
    d_Azure_AD_registered = models.TextField(null=True, blank=True)
    d_EAS_activation_ID = models.TextField(null=True, blank=True)
    d_Serial_number = models.TextField(null=True, blank=True)
    d_Manufacturer = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_EAS_activated = models.TextField(null=True, blank=True)
    d_IMEI = models.TextField(null=True, blank=True)
    d_Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    d_EAS_reason = models.TextField(null=True, blank=True)
    d_EAS_status = models.TextField(null=True, blank=True)
    d_Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    d_Security_patch_level = models.TextField(null=True, blank=True)
    d_WiFi_MAC = models.TextField(null=True, blank=True)
    d_MEID = models.TextField(null=True, blank=True)
    d_Subscriber_carrier = models.TextField(null=True, blank=True)
    d_Total_storage = models.TextField(null=True, blank=True)
    d_Free_storage = models.TextField(null=True, blank=True)
    d_Management_name = models.TextField(null=True, blank=True)
    d_Category = models.TextField(null=True, blank=True)
    d_UserId = models.TextField(null=True, blank=True)
    d_Primary_user_UPN = models.TextField(null=True, blank=True)
    d_Primary_user_email_address = models.TextField(null=True, blank=True)
    d_Primary_user_display_name = models.TextField(null=True, blank=True)
    d_WiFiIPv4Address = models.TextField(null=True, blank=True)
    d_WiFiSubnetID = models.TextField(null=True, blank=True)
    d_Compliance = models.TextField(null=True, blank=True)
    d_Managed_by = models.TextField(null=True, blank=True)
    d_Ownership = models.TextField(null=True, blank=True)
    d_Device_state = models.TextField(null=True, blank=True)
    d_Intune_registered = models.TextField(null=True, blank=True)
    d_Supervised = models.TextField(null=True, blank=True)
    d_Encrypted = models.TextField(null=True, blank=True)
    d_OS = models.TextField(null=True, blank=True)
    d_SkuFamily = models.TextField(null=True, blank=True)
    d_JoinType = models.TextField(null=True, blank=True)
    d_Phone_number = models.TextField(null=True, blank=True)
    d_Jailbroken = models.TextField(null=True, blank=True)
    d_ICCID = models.TextField(null=True, blank=True)
    d_EthernetMAC = models.TextField(null=True, blank=True)
    d_CellularTechnology = models.TextField(null=True, blank=True)
    d_ProcessorArchitecture = models.TextField(null=True, blank=True)
    d_EID = models.TextField(null=True, blank=True)
    d_SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    d_TPMManufacturerId = models.TextField(null=True, blank=True)
    d_TPMManufacturerVersion = models.TextField(null=True, blank=True)
    d_ProductName = models.TextField(null=True, blank=True)
    d_Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 21  # Do not change this value
    date_fields_to_convert = ['d_Last_EAS_sync_time', 'd_Management_certificate_expiration_date', 'd_Compliance_grace_period_expiration', 'Last_device_update', 'First_Seen']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaIntunevsDefender(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Enrollment_date = models.BigIntegerField(null=True, blank=True)
    Last_checkin = models.BigIntegerField(null=True, blank=True)
    Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Azure_AD_registered = models.TextField(null=True, blank=True)
    EAS_activation_ID = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    EAS_activated = models.TextField(null=True, blank=True)
    IMEI = models.TextField(null=True, blank=True)
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    EAS_reason = models.TextField(null=True, blank=True)
    EAS_status = models.TextField(null=True, blank=True)
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    Security_patch_level = models.TextField(null=True, blank=True)
    WiFi_MAC = models.TextField(null=True, blank=True)
    MEID = models.TextField(null=True, blank=True)
    Subscriber_carrier = models.TextField(null=True, blank=True)
    Total_storage = models.TextField(null=True, blank=True)
    Free_storage = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    UserId = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_display_name = models.TextField(null=True, blank=True)
    WiFiIPv4Address = models.TextField(null=True, blank=True)
    WiFiSubnetID = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Intune_registered = models.TextField(null=True, blank=True)
    Supervised = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    SkuFamily = models.TextField(null=True, blank=True)
    JoinType = models.TextField(null=True, blank=True)
    Phone_number = models.TextField(null=True, blank=True)
    Jailbroken = models.TextField(null=True, blank=True)
    ICCID = models.TextField(null=True, blank=True)
    EthernetMAC = models.TextField(null=True, blank=True)
    CellularTechnology = models.TextField(null=True, blank=True)
    ProcessorArchitecture = models.TextField(null=True, blank=True)
    EID = models.TextField(null=True, blank=True)
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    TPMManufacturerId = models.TextField(null=True, blank=True)
    TPMManufacturerVersion = models.TextField(null=True, blank=True)
    ProductName = models.TextField(null=True, blank=True)
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_Name = models.TextField(null=True, blank=True)
    d_Device_Category = models.TextField(null=True, blank=True)
    d_Device_Type = models.TextField(null=True, blank=True)
    d_Device_Subtype = models.TextField(null=True, blank=True)
    d_Discovery_sources = models.TextField(null=True, blank=True)
    d_Domain = models.TextField(null=True, blank=True)
    d_AAD_Device_Id = models.TextField(null=True, blank=True)
    d_First_Seen = models.BigIntegerField(null=True, blank=True)
    d_Last_device_update = models.BigIntegerField(null=True, blank=True)
    d_OS_Platform = models.TextField(null=True, blank=True)
    d_OS_Distribution = models.TextField(null=True, blank=True)
    d_OS_Version = models.TextField(null=True, blank=True)
    d_OS_Build = models.TextField(null=True, blank=True)
    d_Windows_10_Version = models.TextField(null=True, blank=True)
    d_Tags = models.TextField(null=True, blank=True)
    d_Group = models.TextField(null=True, blank=True)
    d_Is_AAD_Joined = models.TextField(null=True, blank=True)
    d_Device_IPs = models.TextField(null=True, blank=True)
    d_Device_MACs = models.TextField(null=True, blank=True)
    d_Risk_Level = models.TextField(null=True, blank=True)
    d_Exposure_Level = models.TextField(null=True, blank=True)
    d_Health_Status = models.TextField(null=True, blank=True)
    d_Onboarding_Status = models.TextField(null=True, blank=True)
    d_Device_Role = models.TextField(null=True, blank=True)
    d_Cloud_Platforms = models.TextField(null=True, blank=True)
    d_Is_Internet_Facing = models.TextField(null=True, blank=True)
    d_Enrollment_Status_Code = models.TextField(null=True, blank=True)
    d_Managed_By = models.TextField(null=True, blank=True)
    d_Enrollment_Status = models.TextField(null=True, blank=True)
    d_Vendor = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_Firmware_versions = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 22  # Do not change this value
    date_fields_to_convert = ['Management_certificate_expiration_date', 'd_First_Seen', 'Last_checkin', 'Enrollment_date', 'Compliance_grace_period_expiration', 'd_Last_device_update', 'Last_EAS_sync_time']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []

class NupayDeltaIntunevsAV(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Enrollment_date = models.BigIntegerField(null=True, blank=True)
    Last_checkin = models.BigIntegerField(null=True, blank=True)
    Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Azure_AD_registered = models.TextField(null=True, blank=True)
    EAS_activation_ID = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    EAS_activated = models.TextField(null=True, blank=True)
    IMEI = models.TextField(null=True, blank=True)
    Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    EAS_reason = models.TextField(null=True, blank=True)
    EAS_status = models.TextField(null=True, blank=True)
    Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    Security_patch_level = models.TextField(null=True, blank=True)
    WiFi_MAC = models.TextField(null=True, blank=True)
    MEID = models.TextField(null=True, blank=True)
    Subscriber_carrier = models.TextField(null=True, blank=True)
    Total_storage = models.TextField(null=True, blank=True)
    Free_storage = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    UserId = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_display_name = models.TextField(null=True, blank=True)
    WiFiIPv4Address = models.TextField(null=True, blank=True)
    WiFiSubnetID = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Intune_registered = models.TextField(null=True, blank=True)
    Supervised = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    SkuFamily = models.TextField(null=True, blank=True)
    JoinType = models.TextField(null=True, blank=True)
    Phone_number = models.TextField(null=True, blank=True)
    Jailbroken = models.TextField(null=True, blank=True)
    ICCID = models.TextField(null=True, blank=True)
    EthernetMAC = models.TextField(null=True, blank=True)
    CellularTechnology = models.TextField(null=True, blank=True)
    ProcessorArchitecture = models.TextField(null=True, blank=True)
    EID = models.TextField(null=True, blank=True)
    SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    TPMManufacturerId = models.TextField(null=True, blank=True)
    TPMManufacturerVersion = models.TextField(null=True, blank=True)
    ProductName = models.TextField(null=True, blank=True)
    Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_name = models.TextField(null=True, blank=True)
    d_Device_group = models.TextField(null=True, blank=True)
    d_OS = models.TextField(null=True, blank=True)
    d_OS_platform = models.TextField(null=True, blank=True)
    d_OS_version = models.TextField(null=True, blank=True)
    d_AV_mode = models.TextField(null=True, blank=True)
    d_Security_intel_version = models.TextField(null=True, blank=True)
    d_Engine_version = models.TextField(null=True, blank=True)
    d_Platform_version = models.TextField(null=True, blank=True)
    d_Quick_scan_status = models.TextField(null=True, blank=True)
    d_Quick_scan_error = models.TextField(null=True, blank=True)
    d_Full_scan_status = models.TextField(null=True, blank=True)
    d_Full_scan_error = models.TextField(null=True, blank=True)
    d_Quick_scan_time = models.BigIntegerField(null=True, blank=True)
    d_Full_scan_time = models.BigIntegerField(null=True, blank=True)
    d_Last_seen = models.BigIntegerField(null=True, blank=True)
    d_Data_refresh_timestamp = models.BigIntegerField(null=True, blank=True)
    d_Engine_update_time = models.BigIntegerField(null=True, blank=True)
    d_Signature_update_time = models.BigIntegerField(null=True, blank=True)
    d_Platform_update_time = models.BigIntegerField(null=True, blank=True)
    d_Security_intelligence_up_to_date = models.TextField(null=True, blank=True)
    d_Engine_up_to_date = models.TextField(null=True, blank=True)
    d_Platform_up_to_date = models.TextField(null=True, blank=True)
    d_Security_intel_publish_time = models.BigIntegerField(null=True, blank=True)
    d_Signature_refresh_time = models.BigIntegerField(null=True, blank=True)
    d_eBPF_status = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 23  # Do not change this value
    date_fields_to_convert = ['d_Signature_update_time', 'd_Platform_update_time', 'd_Last_seen', 'Last_checkin', 'Enrollment_date', 'Last_EAS_sync_time', 'd_Quick_scan_time', 'd_Data_refresh_timestamp', 'd_Engine_update_time', 'd_Security_intel_publish_time', 'd_Signature_refresh_time', 'Management_certificate_expiration_date', 'd_Full_scan_time', 'Compliance_grace_period_expiration']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []

class NuPayDeltaDefendervsIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_Name = models.TextField(null=True, blank=True)
    Device_Category = models.TextField(null=True, blank=True)
    Device_Type = models.TextField(null=True, blank=True)
    Device_Subtype = models.TextField(null=True, blank=True)
    Discovery_sources = models.TextField(null=True, blank=True)
    Domain = models.TextField(null=True, blank=True)
    AAD_Device_Id = models.TextField(null=True, blank=True)
    First_Seen = models.BigIntegerField(null=True, blank=True)
    Last_device_update = models.BigIntegerField(null=True, blank=True)
    OS_Platform = models.TextField(null=True, blank=True)
    OS_Distribution = models.TextField(null=True, blank=True)
    OS_Version = models.TextField(null=True, blank=True)
    OS_Build = models.TextField(null=True, blank=True)
    Windows_10_Version = models.TextField(null=True, blank=True)
    Tags = models.TextField(null=True, blank=True)
    Group = models.TextField(null=True, blank=True)
    Is_AAD_Joined = models.TextField(null=True, blank=True)
    Device_IPs = models.TextField(null=True, blank=True)
    Device_MACs = models.TextField(null=True, blank=True)
    Risk_Level = models.TextField(null=True, blank=True)
    Exposure_Level = models.TextField(null=True, blank=True)
    Health_Status = models.TextField(null=True, blank=True)
    Onboarding_Status = models.TextField(null=True, blank=True)
    Device_Role = models.TextField(null=True, blank=True)
    Cloud_Platforms = models.TextField(null=True, blank=True)
    Is_Internet_Facing = models.TextField(null=True, blank=True)
    Enrollment_Status_Code = models.TextField(null=True, blank=True)
    Managed_By = models.TextField(null=True, blank=True)
    Enrollment_Status = models.TextField(null=True, blank=True)
    Vendor = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Firmware_versions = models.TextField(null=True, blank=True)
    d_DeviceName = models.TextField(null=True, blank=True)
    d_UPN = models.TextField(null=True, blank=True)
    d_ReportStatus = models.TextField(null=True, blank=True)
    d_ReportStatus_loc = models.TextField(null=True, blank=True)
    d_AssignmentFilterIds = models.TextField(null=True, blank=True)
    d_PspdpuLastModifiedTimeUtc = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 24  # Do not change this value
    date_fields_to_convert = ['First_Seen', 'd_PspdpuLastModifiedTimeUtc', 'Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []

class FintechNewEmployess(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Nr = models.TextField(null=True, blank=True, verbose_name='Emp_Nr', db_column='Emp_Nr')
    Employee_Name = models.TextField(null=True, blank=True, verbose_name='Employee_Name', db_column='Employee_Name')
    Surname = models.TextField(null=True, blank=True, verbose_name='Surname', db_column='Surname')
    Start_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Start_Date', db_column='Start_Date')
    Employee_Job_Title = models.TextField(null=True, blank=True, verbose_name='Employee_Job_Title', db_column='Employee_Job_Title')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Start_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Nr = models.TextField(null=True, blank=True, verbose_name='Emp_Nr', db_column='Emp_Nr')
    Employee_Name = models.TextField(null=True, blank=True, verbose_name='Employee_Name', db_column='Employee_Name')
    Surname = models.TextField(null=True, blank=True, verbose_name='Surname', db_column='Surname')
    Start_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Start_Date', db_column='Start_Date')
    Employee_Job_Title = models.TextField(null=True, blank=True, verbose_name='Employee_Job_Title', db_column='Employee_Job_Title')
    Termination_date = models.BigIntegerField(null=True, blank=True, verbose_name='Termination_date', db_column='Termination_date')
    Reason_for_Termination = models.TextField(null=True, blank=True, verbose_name='Reason_for_Termination', db_column='Reason_for_Termination')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Start_Date', 'Termination_date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechMasterEmployeeFile(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Number = models.TextField(null=True, blank=True, verbose_name='Emp_Number', db_column='Emp_Number')
    First_Name = models.TextField(null=True, blank=True, verbose_name='First_Name', db_column='First_Name')
    Last_Name = models.TextField(null=True, blank=True, verbose_name='Last_Name', db_column='Last_Name')
    Group_Join_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Group_Join_Date', db_column='Group_Join_Date')
    Employment_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Employment_Date', db_column='Employment_Date')
    Termination_Date = models.TextField(null=True, blank=True, verbose_name='Termination_Date', db_column='Termination_Date')
    Termination_Reason = models.TextField(null=True, blank=True, verbose_name='Termination_Reason', db_column='Termination_Reason')
    Job_Title = models.TextField(null=True, blank=True, verbose_name='Job_Title', db_column='Job_Title')
    Business_Unit = models.TextField(null=True, blank=True, verbose_name='Business_Unit', db_column='Business_Unit')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Date = models.TextField(null=True, blank=True, verbose_name='Date', db_column='Date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Group_Join_Date', 'Employment_Date',]
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechConsolidatedChanges(models.Model):
    ID = models.AutoField(primary_key=True)
    Item = models.TextField(null=True, blank=True, verbose_name='Item', db_column='Item')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Prepaid3rd_party = models.TextField(null=True, blank=True, verbose_name='Prepaid3rd_party', db_column='Prepaid3rd_party')
    Remedy_Call_No = models.TextField(null=True, blank=True, verbose_name='Remedy_Call_No', db_column='Remedy_Call_No')
    SNOWDevOps_Call_No = models.TextField(null=True, blank=True, verbose_name='SNOWDevOps_Call_No', db_column='SNOWDevOps_Call_No')
    Desc = models.TextField(null=True, blank=True, verbose_name='Desc', db_column='Desc')
    Comments = models.TextField(null=True, blank=True, verbose_name='Comments', db_column='Comments')
    Risk = models.TextField(null=True, blank=True, verbose_name='Risk', db_column='Risk')
    Submitted_By = models.TextField(null=True, blank=True, verbose_name='Submitted_By', db_column='Submitted_By')
    Due_Date = models.TextField(null=True, blank=True, verbose_name='Due_Date', db_column='Due_Date')
    Approved = models.TextField(null=True, blank=True, verbose_name='Approved', db_column='Approved')
    Notes_Updates_31022025 = models.TextField(null=True, blank=True, verbose_name='Notes_Updates_31022025', db_column='Notes_Updates_31022025')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechIncidents(models.Model):
    ID = models.AutoField(primary_key=True)
    incident_number = models.TextField(null=True, blank=True, verbose_name='incident_number', db_column='incident_number')
    company = models.TextField(null=True, blank=True, verbose_name='company', db_column='company')
    first_name = models.TextField(null=True, blank=True, verbose_name='first_name', db_column='first_name')
    last_name = models.TextField(null=True, blank=True, verbose_name='last_name', db_column='last_name')
    z1d_template_name = models.TextField(null=True, blank=True, verbose_name='z1d_template_name', db_column='z1d_template_name')
    description = models.TextField(null=True, blank=True, verbose_name='description', db_column='description')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    assigned_group = models.TextField(null=True, blank=True, verbose_name='assigned_group', db_column='assigned_group')
    assignee = models.TextField(null=True, blank=True, verbose_name='assignee', db_column='assignee')
    Status_Desc = models.TextField(null=True, blank=True, verbose_name='Status_Desc', db_column='Status_Desc')
    Urgency_Desc = models.TextField(null=True, blank=True, verbose_name='Urgency_Desc', db_column='Urgency_Desc')
    categorization_tier_1 = models.TextField(null=True, blank=True, verbose_name='categorization_tier_1', db_column='categorization_tier_1')
    categorization_tier_2 = models.TextField(null=True, blank=True, verbose_name='categorization_tier_2', db_column='categorization_tier_2')
    categorization_tier_3 = models.TextField(null=True, blank=True, verbose_name='categorization_tier_3', db_column='categorization_tier_3')
    closure_product_category_tier1 = models.TextField(null=True, blank=True, verbose_name='closure_product_category_tier1', db_column='closure_product_category_tier1')
    closure_product_category_tier2 = models.TextField(null=True, blank=True, verbose_name='closure_product_category_tier2', db_column='closure_product_category_tier2')
    closure_product_category_tier3 = models.TextField(null=True, blank=True, verbose_name='closure_product_category_tier3', db_column='closure_product_category_tier3')
    product_name = models.TextField(null=True, blank=True, verbose_name='product_name', db_column='product_name')
    resolution = models.TextField(null=True, blank=True, verbose_name='resolution', db_column='resolution')
    ci = models.TextField(null=True, blank=True, verbose_name='ci', db_column='ci')
    next_target_date = models.BigIntegerField(null=True, blank=True, verbose_name='next_target_date', db_column='next_target_date')
    Impact_Desc = models.TextField(null=True, blank=True, verbose_name='Impact_Desc', db_column='Impact_Desc')
    Priority_Desc = models.TextField(null=True, blank=True, verbose_name='Priority_Desc', db_column='Priority_Desc')
    assigned_support_company = models.TextField(null=True, blank=True, verbose_name='assigned_support_company', db_column='assigned_support_company')
    Reported_Source = models.TextField(null=True, blank=True, verbose_name='Reported_Source', db_column='Reported_Source')
    assigned_support_organization = models.TextField(null=True, blank=True, verbose_name='assigned_support_organization', db_column='assigned_support_organization')
    category = models.TextField(null=True, blank=True, verbose_name='category', db_column='category')
    product_categorization_tier_1 = models.TextField(null=True, blank=True, verbose_name='product_categorization_tier_1', db_column='product_categorization_tier_1')
    product_categorization_tier_2 = models.TextField(null=True, blank=True, verbose_name='product_categorization_tier_2', db_column='product_categorization_tier_2')
    product_categorization_tier_3 = models.TextField(null=True, blank=True, verbose_name='product_categorization_tier_3', db_column='product_categorization_tier_3')
    manufacturer = models.TextField(null=True, blank=True, verbose_name='manufacturer', db_column='manufacturer')
    product_model_version = models.TextField(null=True, blank=True, verbose_name='product_model_version', db_column='product_model_version')
    resolution_category = models.TextField(null=True, blank=True, verbose_name='resolution_category', db_column='resolution_category')
    resolution_category_tier_2 = models.TextField(null=True, blank=True, verbose_name='resolution_category_tier_2', db_column='resolution_category_tier_2')
    resolution_category_tier_3 = models.TextField(null=True, blank=True, verbose_name='resolution_category_tier_3', db_column='resolution_category_tier_3')
    closure_product_name = models.TextField(null=True, blank=True, verbose_name='closure_product_name', db_column='closure_product_name')
    closure_manufacturer = models.TextField(null=True, blank=True, verbose_name='closure_manufacturer', db_column='closure_manufacturer')
    closure_product_model_version = models.TextField(null=True, blank=True, verbose_name='closure_product_model_version', db_column='closure_product_model_version')
    group_transfers = models.TextField(null=True, blank=True, verbose_name='group_transfers', db_column='group_transfers')
    total_transfers = models.TextField(null=True, blank=True, verbose_name='total_transfers', db_column='total_transfers')
    individual_transfers = models.TextField(null=True, blank=True, verbose_name='individual_transfers', db_column='individual_transfers')
    Incident_Type = models.TextField(null=True, blank=True, verbose_name='Incident_Type', db_column='Incident_Type')
    Reported_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Reported_Date', db_column='Reported_Date')
    Responed_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Responed_Date', db_column='Responed_Date')
    Closed_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Closed_Date', db_column='Closed_Date')
    submitter = models.TextField(null=True, blank=True, verbose_name='submitter', db_column='submitter')
    owner_support_company = models.TextField(null=True, blank=True, verbose_name='owner_support_company', db_column='owner_support_company')
    owner_support_organization = models.TextField(null=True, blank=True, verbose_name='owner_support_organization', db_column='owner_support_organization')
    owner_group = models.TextField(null=True, blank=True, verbose_name='owner_group', db_column='owner_group')
    owner = models.TextField(null=True, blank=True, verbose_name='owner', db_column='owner')
    detailed_description = models.TextField(null=True, blank=True, verbose_name='detailed_description', db_column='detailed_description')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Submit_Date', 'next_target_date', 'Reported_Date', 'Responed_Date', 'Closed_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechSysproOperatorList(models.Model):
    ID = models.AutoField(primary_key=True)
    Operator = models.TextField(null=True, blank=True, verbose_name='Operator', db_column='Operator')
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Last_login = models.TextField(null=True, blank=True, verbose_name='Last_login', db_column='Last_login')
    Location = models.TextField(null=True, blank=True, verbose_name='Location', db_column='Location')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Primary_role = models.TextField(null=True, blank=True, verbose_name='Primary_role', db_column='Primary_role')
    Primary_group = models.TextField(null=True, blank=True, verbose_name='Primary_group', db_column='Primary_group')
    Date_added = models.BigIntegerField(null=True, blank=True, verbose_name='Date_added', db_column='Date_added')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_added']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechSysproOperatorsList(models.Model):
    ID = models.AutoField(primary_key=True)
    Operator = models.TextField(null=True, blank=True, verbose_name='Operator', db_column='Operator')
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Last_login = models.TextField(null=True, blank=True, verbose_name='Last_login', db_column='Last_login')
    Location = models.TextField(null=True, blank=True, verbose_name='Location', db_column='Location')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Primary_role = models.TextField(null=True, blank=True, verbose_name='Primary_role', db_column='Primary_role')
    Primary_group = models.TextField(null=True, blank=True, verbose_name='Primary_group', db_column='Primary_group')
    Date_added = models.BigIntegerField(null=True, blank=True, verbose_name='Date_added', db_column='Date_added')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_added']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaMasterEmployeevsTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Number = models.TextField(null=True, blank=True)
    First_Name = models.TextField(null=True, blank=True)
    Last_Name = models.TextField(null=True, blank=True)
    Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    Employment_Date = models.BigIntegerField(null=True, blank=True)
    Termination_Date = models.TextField(null=True, blank=True)
    Termination_Reason = models.TextField(null=True, blank=True)
    Job_Title = models.TextField(null=True, blank=True)
    Business_Unit = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Date = models.TextField(null=True, blank=True)
    d_Emp_Nr = models.TextField(null=True, blank=True)
    d_Employee_Name = models.TextField(null=True, blank=True)
    d_Surname = models.TextField(null=True, blank=True)
    d_Start_Date = models.BigIntegerField(null=True, blank=True)
    d_Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Termination_date = models.BigIntegerField(null=True, blank=True)
    d_Reason_for_Termination = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 25  # Do not change this value
    date_fields_to_convert = ['d_Termination_date', 'd_Start_Date', 'Employment_Date', 'Group_Join_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaSysproUserstoterminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Operator = models.TextField(null=True, blank=True)
    Name = models.TextField(null=True, blank=True)
    Last_login = models.TextField(null=True, blank=True)
    Location = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    Primary_role = models.TextField(null=True, blank=True)
    Primary_group = models.TextField(null=True, blank=True)
    Date_added = models.BigIntegerField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    d_Emp_Nr = models.TextField(null=True, blank=True)
    d_Employee_Name = models.TextField(null=True, blank=True)
    d_Surname = models.TextField(null=True, blank=True)
    d_Start_Date = models.BigIntegerField(null=True, blank=True)
    d_Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Termination_date = models.BigIntegerField(null=True, blank=True)
    d_Reason_for_Termination = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 26  # Do not change this value
    date_fields_to_convert = ['d_Termination_date', 'Date_added', 'd_Start_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaNewuserstoMasterHR(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Nr = models.TextField(null=True, blank=True)
    Employee_Name = models.TextField(null=True, blank=True)
    Surname = models.TextField(null=True, blank=True)
    Start_Date = models.BigIntegerField(null=True, blank=True)
    Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Emp_Number = models.TextField(null=True, blank=True)
    d_First_Name = models.TextField(null=True, blank=True)
    d_Last_Name = models.TextField(null=True, blank=True)
    d_Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    d_Employment_Date = models.BigIntegerField(null=True, blank=True)
    d_Termination_Date = models.TextField(null=True, blank=True)
    d_Termination_Reason = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Business_Unit = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Date = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 27  # Do not change this value
    date_fields_to_convert = ['Start_Date', 'd_Employment_Date', 'd_Group_Join_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaNewusersvsTerminatedusers(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Nr = models.TextField(null=True, blank=True)
    Employee_Name = models.TextField(null=True, blank=True)
    Surname = models.TextField(null=True, blank=True)
    Start_Date = models.BigIntegerField(null=True, blank=True)
    Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Emp_Nr = models.TextField(null=True, blank=True)
    d_Employee_Name = models.TextField(null=True, blank=True)
    d_Surname = models.TextField(null=True, blank=True)
    d_Start_Date = models.BigIntegerField(null=True, blank=True)
    d_Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Termination_date = models.BigIntegerField(null=True, blank=True)
    d_Reason_for_Termination = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 28  # Do not change this value
    date_fields_to_convert = ['d_Start_Date', 'd_Termination_date', 'Start_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaNewuserstoMasterHRUsingsurname(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Nr = models.TextField(null=True, blank=True)
    Employee_Name = models.TextField(null=True, blank=True)
    Surname = models.TextField(null=True, blank=True)
    Start_Date = models.BigIntegerField(null=True, blank=True)
    Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Emp_Number = models.TextField(null=True, blank=True)
    d_First_Name = models.TextField(null=True, blank=True)
    d_Last_Name = models.TextField(null=True, blank=True)
    d_Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    d_Employment_Date = models.BigIntegerField(null=True, blank=True)
    d_Termination_Date = models.TextField(null=True, blank=True)
    d_Termination_Reason = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Business_Unit = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Date = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 29  # Do not change this value
    date_fields_to_convert = ['d_Group_Join_Date', 'Start_Date', 'd_Employment_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechCRQCABJun24Jun25vITGC(models.Model):
    ID = models.AutoField(primary_key=True)
    Item = models.TextField(null=True, blank=True, verbose_name='Item', db_column='Item')
    Prepaid3rd_party = models.TextField(null=True, blank=True, verbose_name='Prepaid3rd_party', db_column='Prepaid3rd_party')
    Remedy_Call_No = models.TextField(null=True, blank=True, verbose_name='Remedy_Call_No', db_column='Remedy_Call_No')
    SNOWDevOps_Call_No = models.TextField(null=True, blank=True, verbose_name='SNOWDevOps_Call_No', db_column='SNOWDevOps_Call_No')
    Desc = models.TextField(null=True, blank=True, verbose_name='Desc', db_column='Desc')
    Comments = models.TextField(null=True, blank=True, verbose_name='Comments', db_column='Comments')
    Risk = models.TextField(null=True, blank=True, verbose_name='Risk', db_column='Risk')
    Submitted_By = models.TextField(null=True, blank=True, verbose_name='Submitted_By', db_column='Submitted_By')
    Due_Date = models.TextField(null=True, blank=True, verbose_name='Due_Date', db_column='Due_Date')
    Approved = models.TextField(null=True, blank=True, verbose_name='Approved', db_column='Approved')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Notes_Updates = models.TextField(null=True, blank=True, verbose_name='Notes_Updates', db_column='Notes_Updates')
    N = models.TextField(null=True, blank=True, verbose_name='N', db_column='N')
    Sheet_Name = models.TextField(null=True, blank=True, verbose_name='Sheet_Name', db_column='Sheet_Name')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechMasterEmployeeFileadjusted(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Number = models.TextField(null=True, blank=True, verbose_name='Emp_Number', db_column='Emp_Number')
    First_Name = models.TextField(null=True, blank=True, verbose_name='First_Name', db_column='First_Name')
    Last_Name = models.TextField(null=True, blank=True, verbose_name='Last_Name', db_column='Last_Name')
    Group_Join_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Group_Join_Date', db_column='Group_Join_Date')
    Employment_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Employment_Date', db_column='Employment_Date')
    Termination_Date = models.TextField(null=True, blank=True, verbose_name='Termination_Date', db_column='Termination_Date')
    Termination_Date_no_text = models.BigIntegerField(null=True, blank=True, verbose_name='Termination_Date_no_text', db_column='Termination_Date_no_text')
    Termination_Reason = models.TextField(null=True, blank=True, verbose_name='Termination_Reason', db_column='Termination_Reason')
    Job_Title = models.TextField(null=True, blank=True, verbose_name='Job_Title', db_column='Job_Title')
    Business_Unit = models.TextField(null=True, blank=True, verbose_name='Business_Unit', db_column='Business_Unit')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Date = models.TextField(null=True, blank=True, verbose_name='Date', db_column='Date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Group_Join_Date', 'Employment_Date', 'Termination_Date_no_text']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechAFTCRQClosedwithsubmitdateChangeRequest(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True, verbose_name='Change_ID', db_column='Change_ID')
    Coordinator_Group = models.TextField(null=True, blank=True, verbose_name='Coordinator_Group', db_column='Coordinator_Group')
    Change_Coordinator = models.TextField(null=True, blank=True, verbose_name='Change_Coordinator', db_column='Change_Coordinator')
    Summary = models.TextField(null=True, blank=True, verbose_name='Summary', db_column='Summary')
    Service = models.TextField(null=True, blank=True, verbose_name='Service', db_column='Service')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Impact = models.TextField(null=True, blank=True, verbose_name='Impact', db_column='Impact')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Target_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Target_Date', db_column='Target_Date')
    Product_Categorization_Tier_1 = models.TextField(null=True, blank=True, verbose_name='Product_Categorization_Tier_1', db_column='Product_Categorization_Tier_1')
    Product_Name = models.TextField(null=True, blank=True, verbose_name='Product_Name', db_column='Product_Name')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    Approval_Phase = models.TextField(null=True, blank=True, verbose_name='Approval_Phase', db_column='Approval_Phase')
    Change_Manager = models.TextField(null=True, blank=True, verbose_name='Change_Manager', db_column='Change_Manager')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Target_Date', 'Submit_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AFTCRQClosedwithsubmitdateReportadjusted(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True, verbose_name='Change_ID', db_column='Change_ID')
    Coordinator_Group = models.TextField(null=True, blank=True, verbose_name='Coordinator_Group', db_column='Coordinator_Group')
    Change_Coordinator = models.TextField(null=True, blank=True, verbose_name='Change_Coordinator', db_column='Change_Coordinator')
    Summary = models.TextField(null=True, blank=True, verbose_name='Summary', db_column='Summary')
    Service = models.TextField(null=True, blank=True, verbose_name='Service', db_column='Service')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Impact = models.TextField(null=True, blank=True, verbose_name='Impact', db_column='Impact')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Target_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Target_Date', db_column='Target_Date')
    Product_Categorization_Tier_1 = models.TextField(null=True, blank=True, verbose_name='Product_Categorization_Tier_1', db_column='Product_Categorization_Tier_1')
    Product_Name = models.TextField(null=True, blank=True, verbose_name='Product_Name', db_column='Product_Name')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    Approval_Phase = models.TextField(null=True, blank=True, verbose_name='Approval_Phase', db_column='Approval_Phase')
    Change_Manager = models.TextField(null=True, blank=True, verbose_name='Change_Manager', db_column='Change_Manager')
    Target_Submit_Date_Diff_in_Days = models.IntegerField(null=True, blank=True, verbose_name='Target_Submit_Date_Diff_in_Days', db_column='Target_Submit_Date_Diff_in_Days')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Target_Date', 'Submit_Date']
    integer_fields = ['Target_Submit_Date_Diff_in_Days']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaChangeCoordinatorsvsHRList(models.Model):
    ID = models.AutoField(primary_key=True)



    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 30  # Do not change this value
    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaChangeCoordinatorsvsHRList2(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True)
    Coordinator_Group = models.TextField(null=True, blank=True)
    Change_Coordinator = models.TextField(null=True, blank=True)
    Summary = models.TextField(null=True, blank=True)
    Service = models.TextField(null=True, blank=True)
    Priority = models.TextField(null=True, blank=True)
    Impact = models.TextField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Target_Date = models.BigIntegerField(null=True, blank=True)
    Product_Categorization_Tier_1 = models.TextField(null=True, blank=True)
    Product_Name = models.TextField(null=True, blank=True)
    Submit_Date = models.BigIntegerField(null=True, blank=True)
    Approval_Phase = models.TextField(null=True, blank=True)
    Change_Manager = models.TextField(null=True, blank=True)
    d_Emp_Number = models.TextField(null=True, blank=True)
    d_First_Name = models.TextField(null=True, blank=True)
    d_Last_Name = models.TextField(null=True, blank=True)
    d_Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    d_Employment_Date = models.BigIntegerField(null=True, blank=True)
    d_Termination_Date = models.TextField(null=True, blank=True)
    d_Termination_Reason = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Business_Unit = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Date = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 31  # Do not change this value
    date_fields_to_convert = ['d_Employment_Date', 'd_Group_Join_Date', 'Submit_Date', 'Target_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaChangeCoordinatorsvsTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True)
    Coordinator_Group = models.TextField(null=True, blank=True)
    Change_Coordinator = models.TextField(null=True, blank=True)
    Summary = models.TextField(null=True, blank=True)
    Service = models.TextField(null=True, blank=True)
    Priority = models.TextField(null=True, blank=True)
    Impact = models.TextField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Target_Date = models.BigIntegerField(null=True, blank=True)
    Product_Categorization_Tier_1 = models.TextField(null=True, blank=True)
    Product_Name = models.TextField(null=True, blank=True)
    Submit_Date = models.BigIntegerField(null=True, blank=True)
    Approval_Phase = models.TextField(null=True, blank=True)
    Change_Manager = models.TextField(null=True, blank=True)
    d_Emp_Nr = models.TextField(null=True, blank=True)
    d_Employee_Name = models.TextField(null=True, blank=True)
    d_Surname = models.TextField(null=True, blank=True)
    d_Start_Date = models.BigIntegerField(null=True, blank=True)
    d_Employee_Job_Title = models.TextField(null=True, blank=True)
    d_Termination_date = models.BigIntegerField(null=True, blank=True)
    d_Reason_for_Termination = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 32  # Do not change this value
    date_fields_to_convert = ['Submit_Date', 'Target_Date', 'd_Termination_date', 'd_Start_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class UserADMembership(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    MemberOf = models.TextField(null=True, blank=True, verbose_name='MemberOf', db_column='MemberOf')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADUsers(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    EmailAddress = models.TextField(null=True, blank=True, verbose_name='EmailAddress', db_column='EmailAddress')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    LastLogonDate_Days_Back = models.IntegerField(null=True, blank=True, verbose_name='LastLogonDate_Days_Back', db_column='LastLogonDate_Days_Back')
    Manager = models.TextField(null=True, blank=True, verbose_name='Manager', db_column='Manager')
    OfficePhone = models.TextField(null=True, blank=True, verbose_name='OfficePhone', db_column='OfficePhone')
    Title = models.TextField(null=True, blank=True, verbose_name='Title', db_column='Title')
    Created = models.BigIntegerField(null=True, blank=True, verbose_name='Created', db_column='Created')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    City = models.TextField(null=True, blank=True, verbose_name='City', db_column='City')
    pwdLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet', db_column='pwdLastSet')
    Converted_pwdLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='Converted_pwdLastSet', db_column='Converted_pwdLastSet')
    pwdLastSet_Days_Back = models.IntegerField(null=True, blank=True, verbose_name='pwdLastSet_Days_Back', db_column='pwdLastSet_Days_Back')
    lockoutTime = models.BigIntegerField(null=True, blank=True, verbose_name='lockoutTime', db_column='lockoutTime')
    ConvertedlockoutTime = models.BigIntegerField(null=True, blank=True, verbose_name='ConvertedlockoutTime', db_column='ConvertedlockoutTime')
    employeeID = models.TextField(null=True, blank=True, verbose_name='employeeID', db_column='employeeID')
    displayName = models.TextField(null=True, blank=True, verbose_name='displayName', db_column='displayName')
    givenname = models.TextField(null=True, blank=True, verbose_name='givenname', db_column='givenname')
    sn = models.TextField(null=True, blank=True, verbose_name='sn', db_column='sn')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    userPrincipalName = models.TextField(null=True, blank=True, verbose_name='userPrincipalName', db_column='userPrincipalName')
    mail = models.TextField(null=True, blank=True, verbose_name='mail', db_column='mail')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    EmployeeNumber = models.TextField(null=True, blank=True, verbose_name='EmployeeNumber', db_column='EmployeeNumber')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonDate', 'Created', 'pwdLastSet', 'Converted_pwdLastSet', 'lockoutTime', 'ConvertedlockoutTime']
    integer_fields = ['LastLogonDate_Days_Back', 'pwdLastSet_Days_Back']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['pwdLastSet', 'lockoutTime']


class ADDevices(models.Model):
    ID = models.AutoField(primary_key=True)
    LastLogonTimeStamp = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonTimeStamp', db_column='LastLogonTimeStamp')
    ConvertedLastLogonTimeStamp = models.BigIntegerField(null=True, blank=True, verbose_name='ConvertedLastLogonTimeStamp', db_column='ConvertedLastLogonTimeStamp')
    LastLogonTimeStamp_Days_Back = models.IntegerField(null=True, blank=True, verbose_name='LastLogonTimeStamp_Days_Back', db_column='LastLogonTimeStamp_Days_Back')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    DNSHostName = models.TextField(null=True, blank=True, verbose_name='DNSHostName', db_column='DNSHostName')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    OperatingSystem = models.TextField(null=True, blank=True, verbose_name='OperatingSystem', db_column='OperatingSystem')
    OperatingSystemVersion = models.TextField(null=True, blank=True, verbose_name='OperatingSystemVersion', db_column='OperatingSystemVersion')
    UserPrincipalName = models.TextField(null=True, blank=True, verbose_name='UserPrincipalName', db_column='UserPrincipalName')
    createTimeStamp = models.BigIntegerField(null=True, blank=True, verbose_name='createTimeStamp', db_column='createTimeStamp')
    managedby = models.TextField(null=True, blank=True, verbose_name='managedby', db_column='managedby')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonTimeStamp', 'ConvertedLastLogonTimeStamp', 'createTimeStamp']
    integer_fields = ['LastLogonTimeStamp_Days_Back']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['LastLogonTimeStamp']


class FintechDeltaTerminationsvsAD(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Nr = models.TextField(null=True, blank=True)
    Employee_Name = models.TextField(null=True, blank=True)
    Surname = models.TextField(null=True, blank=True)
    Start_Date = models.BigIntegerField(null=True, blank=True)
    Employee_Job_Title = models.TextField(null=True, blank=True)
    Termination_date = models.BigIntegerField(null=True, blank=True)
    Reason_for_Termination = models.TextField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_EmailAddress = models.TextField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate_Days_Back = models.IntegerField(null=True, blank=True)
    d_Manager = models.TextField(null=True, blank=True)
    d_OfficePhone = models.TextField(null=True, blank=True)
    d_Title = models.TextField(null=True, blank=True)
    d_Created = models.BigIntegerField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_City = models.TextField(null=True, blank=True)
    d_pwdLastSet = models.BigIntegerField(null=True, blank=True)
    d_Converted_pwdLastSet = models.BigIntegerField(null=True, blank=True)
    d_pwdLastSet_Days_Back = models.IntegerField(null=True, blank=True)
    d_lockoutTime = models.BigIntegerField(null=True, blank=True)
    d_ConvertedlockoutTime = models.BigIntegerField(null=True, blank=True)
    d_employeeID = models.TextField(null=True, blank=True)
    d_displayName = models.TextField(null=True, blank=True)
    d_givenname = models.TextField(null=True, blank=True)
    d_sn = models.TextField(null=True, blank=True)
    d_distinguishedName = models.TextField(null=True, blank=True)
    d_userPrincipalName = models.TextField(null=True, blank=True)
    d_mail = models.TextField(null=True, blank=True)
    d_userAccountControl = models.TextField(null=True, blank=True)
    d_usnCreated = models.TextField(null=True, blank=True)
    d_EmployeeNumber = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 33  # Do not change this value
    date_fields_to_convert = ['d_Created', 'd_LastLogonDate', 'd_Converted_pwdLastSet', 'd_pwdLastSet', 'd_lockoutTime', 'd_ConvertedlockoutTime', 'Termination_date', 'Start_Date']
    integer_fields = ['d_LastLogonDate_Days_Back', 'd_pwdLastSet_Days_Back']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['d_pwdLastSet', 'd_lockoutTime']


class FintechDeltaSYsprousersvsAD(models.Model):
    ID = models.AutoField(primary_key=True)
    Operator = models.TextField(null=True, blank=True)
    Name = models.TextField(null=True, blank=True)
    Last_login = models.TextField(null=True, blank=True)
    Location = models.TextField(null=True, blank=True)
    Email = models.TextField(null=True, blank=True)
    Primary_role = models.TextField(null=True, blank=True)
    Primary_group = models.TextField(null=True, blank=True)
    Date_added = models.BigIntegerField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_EmailAddress = models.TextField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate_Days_Back = models.IntegerField(null=True, blank=True)
    d_Manager = models.TextField(null=True, blank=True)
    d_OfficePhone = models.TextField(null=True, blank=True)
    d_Title = models.TextField(null=True, blank=True)
    d_Created = models.BigIntegerField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_City = models.TextField(null=True, blank=True)
    d_pwdLastSet = models.BigIntegerField(null=True, blank=True)
    d_Converted_pwdLastSet = models.BigIntegerField(null=True, blank=True)
    d_pwdLastSet_Days_Back = models.IntegerField(null=True, blank=True)
    d_lockoutTime = models.BigIntegerField(null=True, blank=True)
    d_ConvertedlockoutTime = models.BigIntegerField(null=True, blank=True)
    d_employeeID = models.TextField(null=True, blank=True)
    d_displayName = models.TextField(null=True, blank=True)
    d_givenname = models.TextField(null=True, blank=True)
    d_sn = models.TextField(null=True, blank=True)
    d_distinguishedName = models.TextField(null=True, blank=True)
    d_userPrincipalName = models.TextField(null=True, blank=True)
    d_mail = models.TextField(null=True, blank=True)
    d_userAccountControl = models.TextField(null=True, blank=True)
    d_usnCreated = models.TextField(null=True, blank=True)
    d_EmployeeNumber = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 34  # Do not change this value
    date_fields_to_convert = ['Date_added', 'd_lockoutTime', 'd_Converted_pwdLastSet', 'd_ConvertedlockoutTime', 'd_LastLogonDate', 'd_pwdLastSet', 'd_Created']
    integer_fields = ['d_pwdLastSet_Days_Back', 'd_LastLogonDate_Days_Back']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['d_lockoutTime', 'd_pwdLastSet']


class ADSSoftwareExtract(models.Model):
    ID = models.AutoField(primary_key=True)
    ComputerName_s = models.TextField(null=True, blank=True, verbose_name='ComputerName_s', db_column='ComputerName_s')
    AppName_s = models.TextField(null=True, blank=True, verbose_name='AppName_s', db_column='AppName_s')
    AppPublisher_s = models.TextField(null=True, blank=True, verbose_name='AppPublisher_s', db_column='AppPublisher_s')
    AppVersion_s = models.TextField(null=True, blank=True, verbose_name='AppVersion_s', db_column='AppVersion_s')
    deviceCategoryName = models.TextField(null=True, blank=True, verbose_name='deviceCategoryName', db_column='deviceCategoryName')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaIntunevsSoftwarelist(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Last_checkin = models.BigIntegerField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    d_ComputerName_s = models.TextField(null=True, blank=True)
    d_AppName_s = models.TextField(null=True, blank=True)
    d_AppPublisher_s = models.TextField(null=True, blank=True)
    d_AppVersion_s = models.TextField(null=True, blank=True)
    d_deviceCategoryName = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 35  # Do not change this value
    date_fields_to_convert = ['Last_checkin']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaSoftwarelistvsIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    ComputerName_s = models.TextField(null=True, blank=True)
    AppName_s = models.TextField(null=True, blank=True)
    AppPublisher_s = models.TextField(null=True, blank=True)
    AppVersion_s = models.TextField(null=True, blank=True)
    deviceCategoryName = models.TextField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_name = models.TextField(null=True, blank=True)
    d_Managed_by = models.TextField(null=True, blank=True)
    d_Ownership = models.TextField(null=True, blank=True)
    d_Compliance = models.TextField(null=True, blank=True)
    d_OS = models.TextField(null=True, blank=True)
    d_OS_version = models.TextField(null=True, blank=True)
    d_Device_state = models.TextField(null=True, blank=True)
    d_Primary_user_email_address = models.TextField(null=True, blank=True)
    d_Primary_user_UPN = models.TextField(null=True, blank=True)
    d_Last_checkin = models.BigIntegerField(null=True, blank=True)
    d_Category = models.TextField(null=True, blank=True)
    d_Encrypted = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_Manufacturer = models.TextField(null=True, blank=True)
    d_Serial_number = models.TextField(null=True, blank=True)
    d_Management_name = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 36  # Do not change this value
    date_fields_to_convert = ['d_Last_checkin']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDeltaHRListvsChangeCoordinators(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Number = models.TextField(null=True, blank=True)
    First_Name = models.TextField(null=True, blank=True)
    Last_Name = models.TextField(null=True, blank=True)
    Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    Employment_Date = models.BigIntegerField(null=True, blank=True)
    Termination_Date = models.TextField(null=True, blank=True)
    Termination_Reason = models.TextField(null=True, blank=True)
    Job_Title = models.TextField(null=True, blank=True)
    Business_Unit = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Date = models.TextField(null=True, blank=True)
    d_Change_ID = models.TextField(null=True, blank=True)
    d_Coordinator_Group = models.TextField(null=True, blank=True)
    d_Change_Coordinator = models.TextField(null=True, blank=True)
    d_Summary = models.TextField(null=True, blank=True)
    d_Service = models.TextField(null=True, blank=True)
    d_Priority = models.TextField(null=True, blank=True)
    d_Impact = models.TextField(null=True, blank=True)
    d_Status = models.TextField(null=True, blank=True)
    d_Target_Date = models.BigIntegerField(null=True, blank=True)
    d_Product_Categorization_Tier_1 = models.TextField(null=True, blank=True)
    d_Product_Name = models.TextField(null=True, blank=True)
    d_Submit_Date = models.BigIntegerField(null=True, blank=True)
    d_Approval_Phase = models.TextField(null=True, blank=True)
    d_Change_Manager = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 37  # Do not change this value
    date_fields_to_convert = ['Employment_Date', 'd_Submit_Date', 'd_Target_Date', 'Group_Join_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechdeltaHRVSChangeControllers3(models.Model):
    ID = models.AutoField(primary_key=True)
    Emp_Number = models.TextField(null=True, blank=True)
    First_Name = models.TextField(null=True, blank=True)
    Last_Name = models.TextField(null=True, blank=True)
    Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    Employment_Date = models.BigIntegerField(null=True, blank=True)
    Termination_Date = models.TextField(null=True, blank=True)
    Termination_Reason = models.TextField(null=True, blank=True)
    Job_Title = models.TextField(null=True, blank=True)
    Business_Unit = models.TextField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Date = models.TextField(null=True, blank=True)
    d_Change_ID = models.TextField(null=True, blank=True)
    d_Coordinator_Group = models.TextField(null=True, blank=True)
    d_Change_Coordinator = models.TextField(null=True, blank=True)
    d_Summary = models.TextField(null=True, blank=True)
    d_Service = models.TextField(null=True, blank=True)
    d_Priority = models.TextField(null=True, blank=True)
    d_Impact = models.TextField(null=True, blank=True)
    d_Status = models.TextField(null=True, blank=True)
    d_Target_Date = models.BigIntegerField(null=True, blank=True)
    d_Product_Categorization_Tier_1 = models.TextField(null=True, blank=True)
    d_Product_Name = models.TextField(null=True, blank=True)
    d_Submit_Date = models.BigIntegerField(null=True, blank=True)
    d_Approval_Phase = models.TextField(null=True, blank=True)
    d_Change_Manager = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 38  # Do not change this value
    date_fields_to_convert = ['d_Target_Date', 'Group_Join_Date', 'd_Submit_Date', 'Employment_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AlphalistincTerminations(models.Model):
    ID = models.AutoField(primary_key=True)
    Cost_Centre_Name = models.TextField(null=True, blank=True, verbose_name='Cost_Centre_Name', db_column='Cost_Centre_Name')
    Employee_Number_Disp = models.TextField(null=True, blank=True, verbose_name='Employee_Number_Disp', db_column='Employee_Number_Disp')
    Employee_First_Names = models.TextField(null=True, blank=True, verbose_name='Employee_First_Names', db_column='Employee_First_Names')
    Employee_Known_As = models.TextField(null=True, blank=True, verbose_name='Employee_Known_As', db_column='Employee_Known_As')
    Employee_Surname = models.TextField(null=True, blank=True, verbose_name='Employee_Surname', db_column='Employee_Surname')
    Termination_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Termination_Date', db_column='Termination_Date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class HiresWDJun24toApr25(models.Model):
    ID = models.AutoField(primary_key=True)
    Worker = models.TextField(null=True, blank=True, verbose_name='Worker', db_column='Worker')
    Hire_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Hire_Date', db_column='Hire_Date')
    Reason = models.TextField(null=True, blank=True, verbose_name='Reason', db_column='Reason')
    Supervisory_Organization = models.TextField(null=True, blank=True, verbose_name='Supervisory_Organization', db_column='Supervisory_Organization')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Hire_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class TermsWDJun24toApr25(models.Model):
    ID = models.AutoField(primary_key=True)
    Worker = models.TextField(null=True, blank=True, verbose_name='Worker', db_column='Worker')
    Termination_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Termination_Date', db_column='Termination_Date')
    Supervisory_Organization = models.TextField(null=True, blank=True, verbose_name='Supervisory_Organization', db_column='Supervisory_Organization')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSdeltaHiresvsAlphaHRlist(models.Model):
    ID = models.AutoField(primary_key=True)
    Worker = models.TextField(null=True, blank=True)
    Hire_Date = models.BigIntegerField(null=True, blank=True)
    Reason = models.TextField(null=True, blank=True)
    Supervisory_Organization = models.TextField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 39  # Do not change this value
    date_fields_to_convert = ['d_Termination_Date', 'Hire_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaIntunevsHRMaster(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Last_checkin = models.BigIntegerField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 40  # Do not change this value
    date_fields_to_convert = ['Last_checkin', 'd_Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []
    
    
class ADSADExport2025(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    Creation_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Creation_Date', db_column='Creation_Date')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Disabled = models.TextField(null=True, blank=True, verbose_name='Disabled', db_column='Disabled')
    Display_Name = models.TextField(null=True, blank=True, verbose_name='Display_Name', db_column='Display_Name')
    Email_Address = models.TextField(null=True, blank=True, verbose_name='Email_Address', db_column='Email_Address')
    Employee_ID = models.TextField(null=True, blank=True, verbose_name='Employee_ID', db_column='Employee_ID')
    First_Name = models.TextField(null=True, blank=True, verbose_name='First_Name', db_column='First_Name')
    Job_Title = models.TextField(null=True, blank=True, verbose_name='Job_Title', db_column='Job_Title')
    Last_Logon_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Last_Logon_Date', db_column='Last_Logon_Date')
    Last_Name = models.TextField(null=True, blank=True, verbose_name='Last_Name', db_column='Last_Name')
    Manager = models.TextField(null=True, blank=True, verbose_name='Manager', db_column='Manager')
    Parent_Container_Reversed = models.TextField(null=True, blank=True, verbose_name='Parent_Container_Reversed', db_column='Parent_Container_Reversed')
    Username = models.TextField(null=True, blank=True, verbose_name='Username', db_column='Username')
    Username_pre_2000 = models.TextField(null=True, blank=True, verbose_name='Username_pre_2000', db_column='Username_pre_2000')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Creation_Date', 'Last_Logon_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AsteaChanges2024(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True, verbose_name='Change_ID', db_column='Change_ID')
    Coordinator_Group = models.TextField(null=True, blank=True, verbose_name='Coordinator_Group', db_column='Coordinator_Group')
    Change_Coordinator = models.TextField(null=True, blank=True, verbose_name='Change_Coordinator', db_column='Change_Coordinator')
    Summary = models.TextField(null=True, blank=True, verbose_name='Summary', db_column='Summary')
    Service = models.TextField(null=True, blank=True, verbose_name='Service', db_column='Service')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Impact = models.TextField(null=True, blank=True, verbose_name='Impact', db_column='Impact')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Target_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Target_Date', db_column='Target_Date')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    Submitter = models.TextField(null=True, blank=True, verbose_name='Submitter', db_column='Submitter')
    Class = models.TextField(null=True, blank=True, verbose_name='Class', db_column='Class')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Target_Date', 'Submit_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AsteaChanges2025(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True, verbose_name='Change_ID', db_column='Change_ID')
    Coordinator_Group = models.TextField(null=True, blank=True, verbose_name='Coordinator_Group', db_column='Coordinator_Group')
    Change_Coordinator = models.TextField(null=True, blank=True, verbose_name='Change_Coordinator', db_column='Change_Coordinator')
    Summary = models.TextField(null=True, blank=True, verbose_name='Summary', db_column='Summary')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Impact = models.TextField(null=True, blank=True, verbose_name='Impact', db_column='Impact')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    Submitter = models.TextField(null=True, blank=True, verbose_name='Submitter', db_column='Submitter')
    Class = models.TextField(null=True, blank=True, verbose_name='Class', db_column='Class')
    Customer_Company = models.TextField(null=True, blank=True, verbose_name='Customer_Company', db_column='Customer_Company')
    Change_Location_Company = models.TextField(null=True, blank=True, verbose_name='Change_Location_Company', db_column='Change_Location_Company')
    Scheduled_Start_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Scheduled_Start_Date', db_column='Scheduled_Start_Date')
    Scheduled_End_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Scheduled_End_Date', db_column='Scheduled_End_Date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Submit_Date', 'Scheduled_Start_Date', 'Scheduled_End_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class EmployeesLicenseAllocationsExport20250905164509(models.Model):
    ID = models.AutoField(primary_key=True)
    person_id = models.TextField(null=True, blank=True, verbose_name='person_id', db_column='person_id')
    email_id = models.TextField(null=True, blank=True, verbose_name='email_id', db_column='email_id')
    actgr_id = models.TextField(null=True, blank=True, verbose_name='actgr_id', db_column='actgr_id')
    node_id = models.TextField(null=True, blank=True, verbose_name='node_id', db_column='node_id')
    search_name = models.TextField(null=True, blank=True, verbose_name='search_name', db_column='search_name')
    supervisor_id = models.TextField(null=True, blank=True, verbose_name='supervisor_id', db_column='supervisor_id')
    ap_is_bypass_security = models.TextField(null=True, blank=True, verbose_name='ap_is_bypass_security', db_column='ap_is_bypass_security')
    is_active = models.TextField(null=True, blank=True, verbose_name='is_active', db_column='is_active')
    is_mobile_user = models.TextField(null=True, blank=True, verbose_name='is_mobile_user', db_column='is_mobile_user')
    product_id = models.TextField(null=True, blank=True, verbose_name='product_id', db_column='product_id')
    group_id = models.TextField(null=True, blank=True, verbose_name='group_id', db_column='group_id')
    is_background_person = models.TextField(null=True, blank=True, verbose_name='is_background_person', db_column='is_background_person')
    last_access = models.BigIntegerField(null=True, blank=True, verbose_name='last_access', db_column='last_access')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['last_access']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []



class AsteaTicketsAug2024Aug2025(models.Model):
    ID = models.AutoField(primary_key=True)
    Incident_Number = models.TextField(null=True, blank=True, verbose_name='Incident_Number', db_column='Incident_Number')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    Customer_Name = models.TextField(null=True, blank=True, verbose_name='Customer_Name', db_column='Customer_Name')
    Site = models.TextField(null=True, blank=True, verbose_name='Site', db_column='Site')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    Resolved_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Resolved_Date', db_column='Resolved_Date')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Incident_Type = models.TextField(null=True, blank=True, verbose_name='Incident_Type', db_column='Incident_Type')
    Reported_Source = models.TextField(null=True, blank=True, verbose_name='Reported_Source', db_column='Reported_Source')
    Summary = models.TextField(null=True, blank=True, verbose_name='Summary', db_column='Summary')
    SLM_Measurement_Status = models.TextField(null=True, blank=True, verbose_name='SLM_Measurement_Status', db_column='SLM_Measurement_Status')
    Work_Log_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Work_Log_Date', db_column='Work_Log_Date')
    Last_Work_Info_Update = models.TextField(null=True, blank=True, verbose_name='Last_Work_Info_Update', db_column='Last_Work_Info_Update')
    Closed_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Closed_Date', db_column='Closed_Date')
    Support_Group = models.TextField(null=True, blank=True, verbose_name='Support_Group', db_column='Support_Group')
    Assignee = models.TextField(null=True, blank=True, verbose_name='Assignee', db_column='Assignee')
    Submitter = models.TextField(null=True, blank=True, verbose_name='Submitter', db_column='Submitter')
    Vendor_Group = models.TextField(null=True, blank=True, verbose_name='Vendor_Group', db_column='Vendor_Group')
    Owner_Group = models.TextField(null=True, blank=True, verbose_name='Owner_Group', db_column='Owner_Group')
    Product_Name = models.TextField(null=True, blank=True, verbose_name='Product_Name', db_column='Product_Name')
    Product_Categorization_Tier_3 = models.TextField(null=True, blank=True, verbose_name='Product_Categorization_Tier_3', db_column='Product_Categorization_Tier_3')
    Categorization_Tier_1 = models.TextField(null=True, blank=True, verbose_name='Categorization_Tier_1', db_column='Categorization_Tier_1')
    Categorization_Tier_2 = models.TextField(null=True, blank=True, verbose_name='Categorization_Tier_2', db_column='Categorization_Tier_2')
    Categorization_Tier_3 = models.TextField(null=True, blank=True, verbose_name='Categorization_Tier_3', db_column='Categorization_Tier_3')
    Resolution = models.TextField(null=True, blank=True, verbose_name='Resolution', db_column='Resolution')
    Days_Open = models.IntegerField(null=True, blank=True, verbose_name='Days_Open', db_column='Days_Open')
    Mean_Time_Fix = models.IntegerField(null=True, blank=True, verbose_name='Mean_Time_Fix', db_column='Mean_Time_Fix')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Submit_Date', 'Resolved_Date', 'Work_Log_Date', 'Closed_Date']
    integer_fields = ['Days_Open','Mean_Time_Fix',]
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class AsteaChanges20252024combined(models.Model):
    ID = models.AutoField(primary_key=True)
    Change_ID = models.TextField(null=True, blank=True, verbose_name='Change_ID', db_column='Change_ID')
    Coordinator_Group = models.TextField(null=True, blank=True, verbose_name='Coordinator_Group', db_column='Coordinator_Group')
    Change_Coordinator = models.TextField(null=True, blank=True, verbose_name='Change_Coordinator', db_column='Change_Coordinator')
    Summary = models.TextField(null=True, blank=True, verbose_name='Summary', db_column='Summary')
    Service = models.TextField(null=True, blank=True, verbose_name='Service', db_column='Service')
    Priority = models.TextField(null=True, blank=True, verbose_name='Priority', db_column='Priority')
    Impact = models.TextField(null=True, blank=True, verbose_name='Impact', db_column='Impact')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Target_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Target_Date', db_column='Target_Date')
    Submit_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Submit_Date', db_column='Submit_Date')
    Submitter = models.TextField(null=True, blank=True, verbose_name='Submitter', db_column='Submitter')
    Class = models.TextField(null=True, blank=True, verbose_name='Class', db_column='Class')
    Customer_Company = models.TextField(null=True, blank=True, verbose_name='Customer_Company', db_column='Customer_Company')
    Change_Location_Company = models.TextField(null=True, blank=True, verbose_name='Change_Location_Company', db_column='Change_Location_Company')
    Scheduled_Start_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Scheduled_Start_Date', db_column='Scheduled_Start_Date')
    Scheduled_End_Date = models.BigIntegerField(null=True, blank=True, verbose_name='Scheduled_End_Date', db_column='Scheduled_End_Date')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Target_Date', 'Submit_Date', 'Scheduled_Start_Date', 'Scheduled_End_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaTicketsvsHR(models.Model):
    ID = models.AutoField(primary_key=True)
    Incident_Number = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    Customer_Name = models.TextField(null=True, blank=True)
    Site = models.TextField(null=True, blank=True)
    Submit_Date = models.BigIntegerField(null=True, blank=True)
    Resolved_Date = models.BigIntegerField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Priority = models.TextField(null=True, blank=True)
    Incident_Type = models.TextField(null=True, blank=True)
    Reported_Source = models.TextField(null=True, blank=True)
    Summary = models.TextField(null=True, blank=True)
    SLM_Measurement_Status = models.TextField(null=True, blank=True)
    Work_Log_Date = models.BigIntegerField(null=True, blank=True)
    Last_Work_Info_Update = models.TextField(null=True, blank=True)
    Closed_Date = models.BigIntegerField(null=True, blank=True)
    Support_Group = models.TextField(null=True, blank=True)
    Assignee = models.TextField(null=True, blank=True)
    Submitter = models.TextField(null=True, blank=True)
    Vendor_Group = models.TextField(null=True, blank=True)
    Owner_Group = models.TextField(null=True, blank=True)
    Product_Name = models.TextField(null=True, blank=True)
    Product_Categorization_Tier_3 = models.TextField(null=True, blank=True)
    Categorization_Tier_1 = models.TextField(null=True, blank=True)
    Categorization_Tier_2 = models.TextField(null=True, blank=True)
    Categorization_Tier_3 = models.TextField(null=True, blank=True)
    Resolution = models.TextField(null=True, blank=True)
    Days_Open = models.TextField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 41  # Do not change this value
    date_fields_to_convert = ['Resolved_Date', 'Submit_Date', 'd_Termination_Date', 'Closed_Date', 'Work_Log_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaTicketsvsHR2(models.Model):
    ID = models.AutoField(primary_key=True)
    Incident_Number = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    Customer_Name = models.TextField(null=True, blank=True)
    Site = models.TextField(null=True, blank=True)
    Submit_Date = models.BigIntegerField(null=True, blank=True)
    Closed_Date = models.BigIntegerField(null=True, blank=True)
    Assignee = models.TextField(null=True, blank=True)
    Submitter = models.TextField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 42  # Do not change this value
    date_fields_to_convert = ['Submit_Date', 'Closed_Date', 'd_Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaHRvsAD(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    Creation_Date = models.BigIntegerField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Disabled = models.TextField(null=True, blank=True)
    Display_Name = models.TextField(null=True, blank=True)
    Email_Address = models.TextField(null=True, blank=True)
    Employee_ID = models.TextField(null=True, blank=True)
    First_Name = models.TextField(null=True, blank=True)
    Job_Title = models.TextField(null=True, blank=True)
    Last_Logon_Date = models.BigIntegerField(null=True, blank=True)
    Last_Name = models.TextField(null=True, blank=True)
    Manager = models.TextField(null=True, blank=True)
    Parent_Container_Reversed = models.TextField(null=True, blank=True)
    Username = models.TextField(null=True, blank=True)
    Username_pre_2000 = models.TextField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 43  # Do not change this value
    date_fields_to_convert = ['d_Termination_Date', 'Creation_Date', 'Last_Logon_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaADvsIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True)
    Device_name = models.TextField(null=True, blank=True)
    Managed_by = models.TextField(null=True, blank=True)
    Ownership = models.TextField(null=True, blank=True)
    Compliance = models.TextField(null=True, blank=True)
    OS = models.TextField(null=True, blank=True)
    OS_version = models.TextField(null=True, blank=True)
    Device_state = models.TextField(null=True, blank=True)
    Primary_user_email_address = models.TextField(null=True, blank=True)
    Primary_user_UPN = models.TextField(null=True, blank=True)
    Last_checkin = models.BigIntegerField(null=True, blank=True)
    Category = models.TextField(null=True, blank=True)
    Encrypted = models.TextField(null=True, blank=True)
    Model = models.TextField(null=True, blank=True)
    Manufacturer = models.TextField(null=True, blank=True)
    Serial_number = models.TextField(null=True, blank=True)
    Management_name = models.TextField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_Creation_Date = models.BigIntegerField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Disabled = models.TextField(null=True, blank=True)
    d_Display_Name = models.TextField(null=True, blank=True)
    d_Email_Address = models.TextField(null=True, blank=True)
    d_Employee_ID = models.TextField(null=True, blank=True)
    d_First_Name = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Last_Logon_Date = models.BigIntegerField(null=True, blank=True)
    d_Last_Name = models.TextField(null=True, blank=True)
    d_Manager = models.TextField(null=True, blank=True)
    d_Parent_Container_Reversed = models.TextField(null=True, blank=True)
    d_Username = models.TextField(null=True, blank=True)
    d_Username_pre_2000 = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 44  # Do not change this value
    date_fields_to_convert = ['Last_checkin', 'd_Creation_Date', 'd_Last_Logon_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []
    
    
class ADSADDevices(models.Model):
    ID = models.AutoField(primary_key=True)
    LastLogonTimeStamp = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonTimeStamp', db_column='LastLogonTimeStamp')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    DNSHostName = models.TextField(null=True, blank=True, verbose_name='DNSHostName', db_column='DNSHostName')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    OperatingSystem = models.TextField(null=True, blank=True, verbose_name='OperatingSystem', db_column='OperatingSystem')
    OperatingSystemVersion = models.TextField(null=True, blank=True, verbose_name='OperatingSystemVersion', db_column='OperatingSystemVersion')
    UserPrincipalName = models.TextField(null=True, blank=True, verbose_name='UserPrincipalName', db_column='UserPrincipalName')
    createTimeStamp = models.BigIntegerField(null=True, blank=True, verbose_name='createTimeStamp', db_column='createTimeStamp')
    managedby = models.TextField(null=True, blank=True, verbose_name='managedby', db_column='managedby')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonTimeStamp', 'createTimeStamp']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['LastLogonTimeStamp']


class ADSUserADMemberships(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    MemberOf = models.TextField(null=True, blank=True, verbose_name='MemberOf', db_column='MemberOf')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDeltaLicensesvsHR(models.Model):
    ID = models.AutoField(primary_key=True)
    person_id = models.TextField(null=True, blank=True)
    email_id = models.TextField(null=True, blank=True)
    actgr_id = models.TextField(null=True, blank=True)
    node_id = models.TextField(null=True, blank=True)
    search_name = models.TextField(null=True, blank=True)
    supervisor_id = models.TextField(null=True, blank=True)
    ap_is_bypass_security = models.TextField(null=True, blank=True)
    is_active = models.TextField(null=True, blank=True)
    is_mobile_user = models.TextField(null=True, blank=True)
    product_id = models.TextField(null=True, blank=True)
    group_id = models.TextField(null=True, blank=True)
    is_background_person = models.TextField(null=True, blank=True)
    last_access = models.BigIntegerField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 45  # Do not change this value
    date_fields_to_convert = ['last_access', 'd_Termination_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSADUsers(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    EmailAddress = models.TextField(null=True, blank=True, verbose_name='EmailAddress', db_column='EmailAddress')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    LastLogonDate_Days_Back = models.IntegerField(null=True, blank=True, verbose_name='LastLogonDate_Days_Back', db_column='LastLogonDate_Days_Back')
    Manager = models.TextField(null=True, blank=True, verbose_name='Manager', db_column='Manager')
    OfficePhone = models.TextField(null=True, blank=True, verbose_name='OfficePhone', db_column='OfficePhone')
    Title = models.TextField(null=True, blank=True, verbose_name='Title', db_column='Title')
    Created = models.BigIntegerField(null=True, blank=True, verbose_name='Created', db_column='Created')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    City = models.TextField(null=True, blank=True, verbose_name='City', db_column='City')
    pwdLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet', db_column='pwdLastSet')
    pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet_Converted', db_column='pwdLastSet_Converted')
    pwdLastSet_Days_Back = models.IntegerField(null=True, blank=True, verbose_name='pwdLastSet_Days_Back', db_column='pwdLastSet_Days_Back')
    lockoutTime = models.BigIntegerField(null=True, blank=True, verbose_name='lockoutTime', db_column='lockoutTime')
    lockoutTime_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='lockoutTime_Converted', db_column='lockoutTime_Converted')
    lockoutTime_Days_Back = models.IntegerField(null=True, blank=True, verbose_name='lockoutTime_Days_Back', db_column='lockoutTime_Days_Back')
    employeeID = models.TextField(null=True, blank=True, verbose_name='employeeID', db_column='employeeID')
    displayName = models.TextField(null=True, blank=True, verbose_name='displayName', db_column='displayName')
    givenname = models.TextField(null=True, blank=True, verbose_name='givenname', db_column='givenname')
    sn = models.TextField(null=True, blank=True, verbose_name='sn', db_column='sn')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    userPrincipalName = models.TextField(null=True, blank=True, verbose_name='userPrincipalName', db_column='userPrincipalName')
    mail = models.TextField(null=True, blank=True, verbose_name='mail', db_column='mail')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    EmployeeNumber = models.TextField(null=True, blank=True, verbose_name='EmployeeNumber', db_column='EmployeeNumber')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonDate', 'Created', 'pwdLastSet', 'pwdLastSet_Converted', 'lockoutTime', 'lockoutTime_Converted']
    integer_fields = ['LastLogonDate_Days_Back', 'pwdLastSet_Days_Back', 'lockoutTime_Days_Back']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['pwdLastSet', 'lockoutTime']


class ASECAD(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    EmailAddress = models.TextField(null=True, blank=True, verbose_name='EmailAddress', db_column='EmailAddress')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    LastLogonDate_Days_Back = models.FloatField(null=True, blank=True, verbose_name='LastLogonDate_Days_Back', db_column='LastLogonDate_Days_Back')
    Manager = models.TextField(null=True, blank=True, verbose_name='Manager', db_column='Manager')
    OfficePhone = models.TextField(null=True, blank=True, verbose_name='OfficePhone', db_column='OfficePhone')
    Title = models.TextField(null=True, blank=True, verbose_name='Title', db_column='Title')
    Created = models.BigIntegerField(null=True, blank=True, verbose_name='Created', db_column='Created')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    City = models.TextField(null=True, blank=True, verbose_name='City', db_column='City')
    pwdLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet', db_column='pwdLastSet')
    pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet_Converted', db_column='pwdLastSet_Converted')
    pwdLastSet_Days_Back = models.FloatField(null=True, blank=True, verbose_name='pwdLastSet_Days_Back', db_column='pwdLastSet_Days_Back')
    lockoutTime = models.TextField(null=True, blank=True, verbose_name='lockoutTime', db_column='lockoutTime')
    lockoutTime_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='lockoutTime_Converted', db_column='lockoutTime_Converted')
    lockoutTime_Days_Back = models.FloatField(null=True, blank=True, verbose_name='lockoutTime_Days_Back', db_column='lockoutTime_Days_Back')
    employeeID = models.TextField(null=True, blank=True, verbose_name='employeeID', db_column='employeeID')
    displayName = models.TextField(null=True, blank=True, verbose_name='displayName', db_column='displayName')
    givenname = models.TextField(null=True, blank=True, verbose_name='givenname', db_column='givenname')
    sn = models.TextField(null=True, blank=True, verbose_name='sn', db_column='sn')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    userPrincipalName = models.TextField(null=True, blank=True, verbose_name='userPrincipalName', db_column='userPrincipalName')
    mail = models.TextField(null=True, blank=True, verbose_name='mail', db_column='mail')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    EmployeeNumber = models.TextField(null=True, blank=True, verbose_name='EmployeeNumber', db_column='EmployeeNumber')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonDate', 'Created', 'pwdLastSet', 'lockoutTime_Converted', 'pwdLastSet_Converted']
    integer_fields = []
    float_fields = ['LastLogonDate_Days_Back', 'pwdLastSet_Days_Back', 'lockoutTime_Days_Back']
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ASECDeltaADvsIntune(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True)
    SamAccountName = models.TextField(null=True, blank=True)
    EmailAddress = models.TextField(null=True, blank=True)
    Enabled = models.TextField(null=True, blank=True)
    LastLogonDate = models.BigIntegerField(null=True, blank=True)
    LastLogonDate_Days_Back = models.FloatField(null=True, blank=True)
    Manager = models.TextField(null=True, blank=True)
    OfficePhone = models.TextField(null=True, blank=True)
    Title = models.TextField(null=True, blank=True)
    Created = models.BigIntegerField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    City = models.TextField(null=True, blank=True)
    pwdLastSet = models.BigIntegerField(null=True, blank=True)
    pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True)
    pwdLastSet_Days_Back = models.FloatField(null=True, blank=True)
    lockoutTime = models.TextField(null=True, blank=True)
    lockoutTime_Converted = models.BigIntegerField(null=True, blank=True)
    lockoutTime_Days_Back = models.FloatField(null=True, blank=True)
    employeeID = models.TextField(null=True, blank=True)
    displayName = models.TextField(null=True, blank=True)
    givenname = models.TextField(null=True, blank=True)
    sn = models.TextField(null=True, blank=True)
    distinguishedName = models.TextField(null=True, blank=True)
    userPrincipalName = models.TextField(null=True, blank=True)
    mail = models.TextField(null=True, blank=True)
    userAccountControl = models.TextField(null=True, blank=True)
    usnCreated = models.TextField(null=True, blank=True)
    EmployeeNumber = models.TextField(null=True, blank=True)
    d_Device_ID = models.TextField(null=True, blank=True)
    d_Device_name = models.TextField(null=True, blank=True)
    d_Enrollment_date = models.BigIntegerField(null=True, blank=True)
    d_Last_checkin = models.BigIntegerField(null=True, blank=True)
    d_Azure_AD_Device_ID = models.TextField(null=True, blank=True)
    d_OS_version = models.TextField(null=True, blank=True)
    d_Azure_AD_registered = models.TextField(null=True, blank=True)
    d_EAS_activation_ID = models.TextField(null=True, blank=True)
    d_Serial_number = models.TextField(null=True, blank=True)
    d_Manufacturer = models.TextField(null=True, blank=True)
    d_Model = models.TextField(null=True, blank=True)
    d_EAS_activated = models.TextField(null=True, blank=True)
    d_IMEI = models.TextField(null=True, blank=True)
    d_Last_EAS_sync_time = models.BigIntegerField(null=True, blank=True)
    d_EAS_reason = models.TextField(null=True, blank=True)
    d_EAS_status = models.TextField(null=True, blank=True)
    d_Compliance_grace_period_expiration = models.BigIntegerField(null=True, blank=True)
    d_Security_patch_level = models.TextField(null=True, blank=True)
    d_WiFi_MAC = models.TextField(null=True, blank=True)
    d_MEID = models.TextField(null=True, blank=True)
    d_Subscriber_carrier = models.TextField(null=True, blank=True)
    d_Total_storage = models.TextField(null=True, blank=True)
    d_Free_storage = models.TextField(null=True, blank=True)
    d_Management_name = models.TextField(null=True, blank=True)
    d_Category = models.TextField(null=True, blank=True)
    d_UserId = models.TextField(null=True, blank=True)
    d_Primary_user_UPN = models.TextField(null=True, blank=True)
    d_Primary_user_email_address = models.TextField(null=True, blank=True)
    d_Primary_user_display_name = models.TextField(null=True, blank=True)
    d_WiFiIPv4Address = models.TextField(null=True, blank=True)
    d_WiFiSubnetID = models.TextField(null=True, blank=True)
    d_Compliance = models.TextField(null=True, blank=True)
    d_Managed_by = models.TextField(null=True, blank=True)
    d_Ownership = models.TextField(null=True, blank=True)
    d_Device_state = models.TextField(null=True, blank=True)
    d_Intune_registered = models.TextField(null=True, blank=True)
    d_Supervised = models.TextField(null=True, blank=True)
    d_Encrypted = models.TextField(null=True, blank=True)
    d_OS = models.TextField(null=True, blank=True)
    d_SkuFamily = models.TextField(null=True, blank=True)
    d_JoinType = models.TextField(null=True, blank=True)
    d_Phone_number = models.TextField(null=True, blank=True)
    d_Jailbroken = models.TextField(null=True, blank=True)
    d_ICCID = models.TextField(null=True, blank=True)
    d_EthernetMAC = models.TextField(null=True, blank=True)
    d_CellularTechnology = models.TextField(null=True, blank=True)
    d_ProcessorArchitecture = models.TextField(null=True, blank=True)
    d_EID = models.TextField(null=True, blank=True)
    d_SystemManagementBIOSVersion = models.TextField(null=True, blank=True)
    d_TPMManufacturerId = models.TextField(null=True, blank=True)
    d_TPMManufacturerVersion = models.TextField(null=True, blank=True)
    d_ProductName = models.TextField(null=True, blank=True)
    d_Management_certificate_expiration_date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 46  # Do not change this value
    date_fields_to_convert = ['Created', 'd_Compliance_grace_period_expiration', 'd_Last_checkin', 'lockoutTime_Converted', 'd_Enrollment_date', 'LastLogonDate', 'pwdLastSet_Converted', 'd_Management_certificate_expiration_date', 'd_Last_EAS_sync_time', 'pwdLastSet']
    integer_fields = []
    float_fields = ['LastLogonDate_Days_Back', 'pwdLastSet_Days_Back', 'lockoutTime_Days_Back']
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []

    
class AgentSCBCKCombined(models.Model):
    ID = models.AutoField(primary_key=True)
    Date = models.BigIntegerField(null=True, blank=True, verbose_name='Date', db_column='Date')
    Log = models.TextField(null=True, blank=True, verbose_name='Log', db_column='Log')
    FileName = models.TextField(null=True, blank=True, verbose_name='FileName', db_column='FileName')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechPatchCompliance(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    OSArchitecture = models.TextField(null=True, blank=True, verbose_name='OSArchitecture', db_column='OSArchitecture')
    OSVersion = models.TextField(null=True, blank=True, verbose_name='OSVersion', db_column='OSVersion')
    OSBuild = models.TextField(null=True, blank=True, verbose_name='OSBuild', db_column='OSBuild')
    OSEdition = models.TextField(null=True, blank=True, verbose_name='OSEdition', db_column='OSEdition')
    OSFeatureUpdateStatus = models.TextField(null=True, blank=True, verbose_name='OSFeatureUpdateStatus', db_column='OSFeatureUpdateStatus')
    OSQualityUpdateStatus = models.TextField(null=True, blank=True, verbose_name='OSQualityUpdateStatus', db_column='OSQualityUpdateStatus')
    OSSecurityUpdateStatus = models.TextField(null=True, blank=True, verbose_name='OSSecurityUpdateStatus', db_column='OSSecurityUpdateStatus')
    OSServicingChannel = models.TextField(null=True, blank=True, verbose_name='OSServicingChannel', db_column='OSServicingChannel')
    deviceCategoryName = models.TextField(null=True, blank=True, verbose_name='deviceCategoryName', db_column='deviceCategoryName')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechDevices60days(models.Model):
    ID = models.AutoField(primary_key=True)
    deviceName = models.TextField(null=True, blank=True, verbose_name='deviceName', db_column='deviceName')
    userPrincipalName = models.TextField(null=True, blank=True, verbose_name='userPrincipalName', db_column='userPrincipalName')
    osVersion = models.TextField(null=True, blank=True, verbose_name='osVersion', db_column='osVersion')
    lastSyncDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='lastSyncDateTime', db_column='lastSyncDateTime')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['lastSyncDateTime']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DevicecontrolMicrosoftDefender(models.Model):
    ID = models.AutoField(primary_key=True)
    Date = models.BigIntegerField(null=True, blank=True, verbose_name='Date', db_column='Date')
    Policy = models.TextField(null=True, blank=True, verbose_name='Policy', db_column='Policy')
    Media_name = models.TextField(null=True, blank=True, verbose_name='Media_name', db_column='Media_name')
    Media_class_name = models.TextField(null=True, blank=True, verbose_name='Media_class_name', db_column='Media_class_name')
    Device_name = models.TextField(null=True, blank=True, verbose_name='Device_name', db_column='Device_name')
    User = models.TextField(null=True, blank=True, verbose_name='User', db_column='User')
    Device_Id = models.TextField(null=True, blank=True, verbose_name='Device_Id', db_column='Device_Id')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class SyspOperatorListadj(models.Model):
    ID = models.AutoField(primary_key=True)
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Primary_role = models.TextField(null=True, blank=True, verbose_name='Primary_role', db_column='Primary_role')
    Primary_group = models.TextField(null=True, blank=True, verbose_name='Primary_group', db_column='Primary_group')
    Date_added = models.BigIntegerField(null=True, blank=True, verbose_name='Date_added', db_column='Date_added')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Employee_Number = models.TextField(null=True, blank=True, verbose_name='Employee_Number', db_column='Employee_Number')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Date_added']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class UseradFintech(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    EmailAddress = models.TextField(null=True, blank=True, verbose_name='EmailAddress', db_column='EmailAddress')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    LastLogonDate_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='LastLogonDate_DaysBack', db_column='LastLogonDate_DaysBack')
    Manager = models.TextField(null=True, blank=True, verbose_name='Manager', db_column='Manager')
    OfficePhone = models.TextField(null=True, blank=True, verbose_name='OfficePhone', db_column='OfficePhone')
    Title = models.TextField(null=True, blank=True, verbose_name='Title', db_column='Title')
    Created = models.BigIntegerField(null=True, blank=True, verbose_name='Created', db_column='Created')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    City = models.TextField(null=True, blank=True, verbose_name='City', db_column='City')
    pwdLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet', db_column='pwdLastSet')
    pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet_Converted', db_column='pwdLastSet_Converted')
    pwdLastSet_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='pwdLastSet_DaysBack', db_column='pwdLastSet_DaysBack')
    lockoutTime = models.TextField(null=True, blank=True, verbose_name='lockoutTime', db_column='lockoutTime')
    employeeID = models.TextField(null=True, blank=True, verbose_name='employeeID', db_column='employeeID')
    displayName = models.TextField(null=True, blank=True, verbose_name='displayName', db_column='displayName')
    givenname = models.TextField(null=True, blank=True, verbose_name='givenname', db_column='givenname')
    sn = models.TextField(null=True, blank=True, verbose_name='sn', db_column='sn')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    userPrincipalName = models.TextField(null=True, blank=True, verbose_name='userPrincipalName', db_column='userPrincipalName')
    mail = models.TextField(null=True, blank=True, verbose_name='mail', db_column='mail')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    EmployeeNumber = models.TextField(null=True, blank=True, verbose_name='EmployeeNumber', db_column='EmployeeNumber')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonDate', 'pwdLastSet', 'pwdLastSet_Converted','Created',]
    integer_fields = ['LastLogonDate_DaysBack', 'pwdLastSet_DaysBack']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['pwdLastSet']




class UseradmembershipsFintec(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    MemberOf = models.TextField(null=True, blank=True, verbose_name='MemberOf', db_column='MemberOf')
    D = models.TextField(null=True, blank=True, verbose_name='D', db_column='D')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaFintechNewSysprovsADusers(models.Model):
    ID = models.AutoField(primary_key=True)
    Email = models.TextField(null=True, blank=True)
    Primary_role = models.TextField(null=True, blank=True)
    Primary_group = models.TextField(null=True, blank=True)
    Date_added = models.BigIntegerField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Employee_Number = models.TextField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_EmailAddress = models.TextField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate_DaysBack = models.IntegerField(null=True, blank=True)
    d_Manager = models.TextField(null=True, blank=True)
    d_OfficePhone = models.TextField(null=True, blank=True)
    d_Title = models.TextField(null=True, blank=True)
    d_Created = models.BigIntegerField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_City = models.TextField(null=True, blank=True)
    d_pwdLastSet = models.BigIntegerField(null=True, blank=True)
    d_pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True)
    d_pwdLastSet_DaysBack = models.IntegerField(null=True, blank=True)
    d_lockoutTime = models.TextField(null=True, blank=True)
    d_employeeID = models.TextField(null=True, blank=True)
    d_displayName = models.TextField(null=True, blank=True)
    d_givenname = models.TextField(null=True, blank=True)
    d_sn = models.TextField(null=True, blank=True)
    d_distinguishedName = models.TextField(null=True, blank=True)
    d_userPrincipalName = models.TextField(null=True, blank=True)
    d_mail = models.TextField(null=True, blank=True)
    d_userAccountControl = models.TextField(null=True, blank=True)
    d_usnCreated = models.TextField(null=True, blank=True)
    d_EmployeeNumber = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 47  # Do not change this value
    date_fields_to_convert = ['d_pwdLastSet', 'Date_added', 'd_LastLogonDate', 'd_pwdLastSet_Converted', 'd_Created']
    integer_fields = ['d_LastLogonDate_DaysBack', 'd_pwdLastSet_DaysBack']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['d_pwdLastSet']


class ADSDeltaADvsHR(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True)
    Company = models.TextField(null=True, blank=True)
    Creation_Date = models.BigIntegerField(null=True, blank=True)
    Department = models.TextField(null=True, blank=True)
    Disabled = models.TextField(null=True, blank=True)
    Display_Name = models.TextField(null=True, blank=True)
    Email_Address = models.TextField(null=True, blank=True)
    Employee_ID = models.TextField(null=True, blank=True)
    First_Name = models.TextField(null=True, blank=True)
    Job_Title = models.TextField(null=True, blank=True)
    Last_Logon_Date = models.BigIntegerField(null=True, blank=True)
    Last_Name = models.TextField(null=True, blank=True)
    Manager = models.TextField(null=True, blank=True)
    Parent_Container_Reversed = models.TextField(null=True, blank=True)
    Username = models.TextField(null=True, blank=True)
    Username_pre_2000 = models.TextField(null=True, blank=True)
    d_Cost_Centre_Name = models.TextField(null=True, blank=True)
    d_Employee_Number_Disp = models.TextField(null=True, blank=True)
    d_Employee_First_Names = models.TextField(null=True, blank=True)
    d_Employee_Known_As = models.TextField(null=True, blank=True)
    d_Employee_Surname = models.TextField(null=True, blank=True)
    d_Termination_Date = models.BigIntegerField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 48  # Do not change this value
    date_fields_to_convert = ['Last_Logon_Date', 'd_Termination_Date', 'Creation_Date']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class DeltaFintechNewNewusersSysprotoHRMaster(models.Model):
    ID = models.AutoField(primary_key=True)
    Email = models.TextField(null=True, blank=True)
    Primary_role = models.TextField(null=True, blank=True)
    Primary_group = models.TextField(null=True, blank=True)
    Date_added = models.BigIntegerField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Employee_Number = models.TextField(null=True, blank=True)
    d_Emp_Number = models.TextField(null=True, blank=True)
    d_First_Name = models.TextField(null=True, blank=True)
    d_Last_Name = models.TextField(null=True, blank=True)
    d_Group_Join_Date = models.BigIntegerField(null=True, blank=True)
    d_Employment_Date = models.BigIntegerField(null=True, blank=True)
    d_Termination_Date = models.TextField(null=True, blank=True)
    d_Termination_Date_no_text = models.BigIntegerField(null=True, blank=True)
    d_Termination_Reason = models.TextField(null=True, blank=True)
    d_Job_Title = models.TextField(null=True, blank=True)
    d_Business_Unit = models.TextField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Date = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 49  # Do not change this value
    date_fields_to_convert = ['d_Employment_Date', 'Date_added', 'd_Group_Join_Date', 'd_Termination_Date_no_text']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []

    
class FintechNewEntraReport(models.Model):
    ID = models.AutoField(primary_key=True)
    displayName = models.TextField(null=True, blank=True, verbose_name='displayName', db_column='displayName')
    accountEnabled = models.TextField(null=True, blank=True, verbose_name='accountEnabled', db_column='accountEnabled')
    operatingSystem = models.TextField(null=True, blank=True, verbose_name='operatingSystem', db_column='operatingSystem')
    operatingSystemVersion = models.TextField(null=True, blank=True, verbose_name='operatingSystemVersion', db_column='operatingSystemVersion')
    joinType_trustType = models.TextField(null=True, blank=True, verbose_name='joinType_trustType', db_column='joinType_trustType')
    registeredOwners = models.TextField(null=True, blank=True, verbose_name='registeredOwners', db_column='registeredOwners')
    userNames = models.TextField(null=True, blank=True, verbose_name='userNames', db_column='userNames')
    mdmDisplayName = models.TextField(null=True, blank=True, verbose_name='mdmDisplayName', db_column='mdmDisplayName')
    isCompliant = models.TextField(null=True, blank=True, verbose_name='isCompliant', db_column='isCompliant')
    registrationTime = models.BigIntegerField(null=True, blank=True, verbose_name='registrationTime', db_column='registrationTime')
    registrationTime_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='registrationTime_DaysBack', db_column='registrationTime_DaysBack')
    approximateLastSignInDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='approximateLastSignInDateTime', db_column='approximateLastSignInDateTime')
    approximateLastSignInDateTime_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='approximateLastSignInDateTime_DaysBack', db_column='approximateLastSignInDateTime_DaysBack')
    deviceId = models.TextField(null=True, blank=True, verbose_name='deviceId', db_column='deviceId')
    isManaged = models.TextField(null=True, blank=True, verbose_name='isManaged', db_column='isManaged')
    objectId = models.TextField(null=True, blank=True, verbose_name='objectId', db_column='objectId')
    profileType = models.TextField(null=True, blank=True, verbose_name='profileType', db_column='profileType')
    systemLabels = models.TextField(null=True, blank=True, verbose_name='systemLabels', db_column='systemLabels')
    model = models.TextField(null=True, blank=True, verbose_name='model', db_column='model')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['registrationTime', 'approximateLastSignInDateTime']
    integer_fields = ['registrationTime_DaysBack', 'approximateLastSignInDateTime_DaysBack']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechNewStaffListing(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Employee_Number = models.TextField(null=True, blank=True, verbose_name='Employee_Number', db_column='Employee_Number')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = []
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechNewSysproOperatorList(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    Network_user_name = models.TextField(null=True, blank=True, verbose_name='Network_user_name', db_column='Network_user_name')
    Operator = models.TextField(null=True, blank=True, verbose_name='Operator', db_column='Operator')
    Location = models.TextField(null=True, blank=True, verbose_name='Location', db_column='Location')
    Employee_Number = models.TextField(null=True, blank=True, verbose_name='Employee_Number', db_column='Employee_Number')
    ExternalInternal = models.TextField(null=True, blank=True, verbose_name='ExternalInternal', db_column='ExternalInternal')
    Primary_group = models.TextField(null=True, blank=True, verbose_name='Primary_group', db_column='Primary_group')
    Last_login = models.TextField(null=True, blank=True, verbose_name='Last_login', db_column='Last_login')
    Last_login_date = models.BigIntegerField(null=True, blank=True, verbose_name='Last_login_date', db_column='Last_login_date')
    Last_login_date_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='Last_login_date_DaysBack', db_column='Last_login_date_DaysBack')
    Date_added = models.BigIntegerField(null=True, blank=True, verbose_name='Date_added', db_column='Date_added')
    Date_added_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='Date_added_DaysBack', db_column='Date_added_DaysBack')
    Date_status_changed = models.BigIntegerField(null=True, blank=True, verbose_name='Date_status_changed', db_column='Date_status_changed')
    Date_status_changed_DaysBack = models.IntegerField(null=True, blank=True, verbose_name='Date_status_changed_DaysBack', db_column='Date_status_changed_DaysBack')
    Status = models.TextField(null=True, blank=True, verbose_name='Status', db_column='Status')
    Account_Locked = models.TextField(null=True, blank=True, verbose_name='Account_Locked', db_column='Account_Locked')
    Email = models.TextField(null=True, blank=True, verbose_name='Email', db_column='Email')
    Status_reason = models.TextField(null=True, blank=True, verbose_name='Status_reason', db_column='Status_reason')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Last_login_date', 'Date_added', 'Date_status_changed']
    integer_fields = ['Last_login_date_DaysBack', 'Date_added_DaysBack', 'Date_status_changed_DaysBack']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class FintechNewUserAD(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.TextField(null=True, blank=True, verbose_name='Name', db_column='Name')
    SamAccountName = models.TextField(null=True, blank=True, verbose_name='SamAccountName', db_column='SamAccountName')
    EmailAddress = models.TextField(null=True, blank=True, verbose_name='EmailAddress', db_column='EmailAddress')
    Enabled = models.TextField(null=True, blank=True, verbose_name='Enabled', db_column='Enabled')
    LastLogonDate = models.BigIntegerField(null=True, blank=True, verbose_name='LastLogonDate', db_column='LastLogonDate')
    Manager = models.TextField(null=True, blank=True, verbose_name='Manager', db_column='Manager')
    OfficePhone = models.TextField(null=True, blank=True, verbose_name='OfficePhone', db_column='OfficePhone')
    Title = models.TextField(null=True, blank=True, verbose_name='Title', db_column='Title')
    Created = models.BigIntegerField(null=True, blank=True, verbose_name='Created', db_column='Created')
    Department = models.TextField(null=True, blank=True, verbose_name='Department', db_column='Department')
    Company = models.TextField(null=True, blank=True, verbose_name='Company', db_column='Company')
    City = models.TextField(null=True, blank=True, verbose_name='City', db_column='City')
    pwdLastSet = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet', db_column='pwdLastSet')
    pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True, verbose_name='pwdLastSet_Converted', db_column='pwdLastSet_Converted')
    lockoutTime = models.BigIntegerField(null=True, blank=True, verbose_name='lockoutTime', db_column='lockoutTime')
    employeeID = models.TextField(null=True, blank=True, verbose_name='employeeID', db_column='employeeID')
    displayName = models.TextField(null=True, blank=True, verbose_name='displayName', db_column='displayName')
    givenname = models.TextField(null=True, blank=True, verbose_name='givenname', db_column='givenname')
    sn = models.TextField(null=True, blank=True, verbose_name='sn', db_column='sn')
    distinguishedName = models.TextField(null=True, blank=True, verbose_name='distinguishedName', db_column='distinguishedName')
    userPrincipalName = models.TextField(null=True, blank=True, verbose_name='userPrincipalName', db_column='userPrincipalName')
    mail = models.TextField(null=True, blank=True, verbose_name='mail', db_column='mail')
    userAccountControl = models.TextField(null=True, blank=True, verbose_name='userAccountControl', db_column='userAccountControl')
    usnCreated = models.TextField(null=True, blank=True, verbose_name='usnCreated', db_column='usnCreated')
    EmployeeNumber = models.TextField(null=True, blank=True, verbose_name='EmployeeNumber', db_column='EmployeeNumber')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastLogonDate', 'Created', 'pwdLastSet', 'pwdLastSet_Converted', 'lockoutTime']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['pwdLastSet','lockoutTime']


class DELTAADSLicensesvsAD(models.Model):
    ID = models.AutoField(primary_key=True)
    person_id = models.TextField(null=True, blank=True)
    email_id = models.TextField(null=True, blank=True)
    actgr_id = models.TextField(null=True, blank=True)
    node_id = models.TextField(null=True, blank=True)
    search_name = models.TextField(null=True, blank=True)
    supervisor_id = models.TextField(null=True, blank=True)
    ap_is_bypass_security = models.TextField(null=True, blank=True)
    is_active = models.TextField(null=True, blank=True)
    is_mobile_user = models.TextField(null=True, blank=True)
    product_id = models.TextField(null=True, blank=True)
    group_id = models.TextField(null=True, blank=True)
    is_background_person = models.TextField(null=True, blank=True)
    last_access = models.BigIntegerField(null=True, blank=True)
    d_Name = models.TextField(null=True, blank=True)
    d_SamAccountName = models.TextField(null=True, blank=True)
    d_EmailAddress = models.TextField(null=True, blank=True)
    d_Enabled = models.TextField(null=True, blank=True)
    d_LastLogonDate = models.BigIntegerField(null=True, blank=True)
    d_LastLogonDate_Days_Back = models.IntegerField(null=True, blank=True)
    d_Manager = models.TextField(null=True, blank=True)
    d_OfficePhone = models.TextField(null=True, blank=True)
    d_Title = models.TextField(null=True, blank=True)
    d_Created = models.BigIntegerField(null=True, blank=True)
    d_Department = models.TextField(null=True, blank=True)
    d_Company = models.TextField(null=True, blank=True)
    d_City = models.TextField(null=True, blank=True)
    d_pwdLastSet = models.BigIntegerField(null=True, blank=True)
    d_pwdLastSet_Converted = models.BigIntegerField(null=True, blank=True)
    d_pwdLastSet_Days_Back = models.IntegerField(null=True, blank=True)
    d_lockoutTime = models.BigIntegerField(null=True, blank=True)
    d_lockoutTime_Converted = models.BigIntegerField(null=True, blank=True)
    d_lockoutTime_Days_Back = models.IntegerField(null=True, blank=True)
    d_employeeID = models.TextField(null=True, blank=True)
    d_displayName = models.TextField(null=True, blank=True)
    d_givenname = models.TextField(null=True, blank=True)
    d_sn = models.TextField(null=True, blank=True)
    d_distinguishedName = models.TextField(null=True, blank=True)
    d_userPrincipalName = models.TextField(null=True, blank=True)
    d_mail = models.TextField(null=True, blank=True)
    d_userAccountControl = models.TextField(null=True, blank=True)
    d_usnCreated = models.TextField(null=True, blank=True)
    d_EmployeeNumber = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 50  # Do not change this value
    date_fields_to_convert = ['d_Created', 'd_lockoutTime', 'd_pwdLastSet', 'd_pwdLastSet_Converted', 'd_lockoutTime_Converted', 'd_LastLogonDate', 'last_access']
    integer_fields = ['d_LastLogonDate_Days_Back', 'd_lockoutTime_Days_Back', 'd_pwdLastSet_Days_Back']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = ['d_lockoutTime', 'd_pwdLastSet']


class ADSDefenderAgents(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    DeviceState = models.TextField(null=True, blank=True, verbose_name='DeviceState', db_column='DeviceState')
    DeviceState_loc = models.TextField(null=True, blank=True, verbose_name='DeviceState_loc', db_column='DeviceState_loc')
    _ManagedBy = models.TextField(null=True, blank=True, verbose_name='_ManagedBy', db_column='_ManagedBy')
    _ManagedBy_loc = models.TextField(null=True, blank=True, verbose_name='_ManagedBy_loc', db_column='_ManagedBy_loc')
    AntiMalwareVersion = models.TextField(null=True, blank=True, verbose_name='AntiMalwareVersion', db_column='AntiMalwareVersion')
    CriticalFailure = models.TextField(null=True, blank=True, verbose_name='CriticalFailure', db_column='CriticalFailure')
    ProductStatus = models.TextField(null=True, blank=True, verbose_name='ProductStatus', db_column='ProductStatus')
    TamperProtectionEnabled = models.TextField(null=True, blank=True, verbose_name='TamperProtectionEnabled', db_column='TamperProtectionEnabled')
    IsVirtualMachine = models.TextField(null=True, blank=True, verbose_name='IsVirtualMachine', db_column='IsVirtualMachine')
    IsWDATPSenseRunning = models.TextField(null=True, blank=True, verbose_name='IsWDATPSenseRunning', db_column='IsWDATPSenseRunning')
    WDATPOnboardingState = models.TextField(null=True, blank=True, verbose_name='WDATPOnboardingState', db_column='WDATPOnboardingState')
    EngineVersion = models.TextField(null=True, blank=True, verbose_name='EngineVersion', db_column='EngineVersion')
    FullScanOverdue = models.TextField(null=True, blank=True, verbose_name='FullScanOverdue', db_column='FullScanOverdue')
    FullScanRequired = models.TextField(null=True, blank=True, verbose_name='FullScanRequired', db_column='FullScanRequired')
    LastFullScanDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='LastFullScanDateTime', db_column='LastFullScanDateTime')
    LastQuickScanDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='LastQuickScanDateTime', db_column='LastQuickScanDateTime')
    LastQuickScanSignatureVersion = models.TextField(null=True, blank=True, verbose_name='LastQuickScanSignatureVersion', db_column='LastQuickScanSignatureVersion')
    LastReportedDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='LastReportedDateTime', db_column='LastReportedDateTime')
    MalwareProtectionEnabled = models.TextField(null=True, blank=True, verbose_name='MalwareProtectionEnabled', db_column='MalwareProtectionEnabled')
    NetworkInspectionSystemEnabled = models.TextField(null=True, blank=True, verbose_name='NetworkInspectionSystemEnabled', db_column='NetworkInspectionSystemEnabled')
    PendingFullScan = models.TextField(null=True, blank=True, verbose_name='PendingFullScan', db_column='PendingFullScan')
    PendingManualSteps = models.TextField(null=True, blank=True, verbose_name='PendingManualSteps', db_column='PendingManualSteps')
    PendingOfflineScan = models.TextField(null=True, blank=True, verbose_name='PendingOfflineScan', db_column='PendingOfflineScan')
    PendingReboot = models.TextField(null=True, blank=True, verbose_name='PendingReboot', db_column='PendingReboot')
    QuickScanOverdue = models.TextField(null=True, blank=True, verbose_name='QuickScanOverdue', db_column='QuickScanOverdue')
    RealTimeProtectionEnabled = models.TextField(null=True, blank=True, verbose_name='RealTimeProtectionEnabled', db_column='RealTimeProtectionEnabled')
    RebootRequired = models.TextField(null=True, blank=True, verbose_name='RebootRequired', db_column='RebootRequired')
    SignatureUpdateOverdue = models.TextField(null=True, blank=True, verbose_name='SignatureUpdateOverdue', db_column='SignatureUpdateOverdue')
    SignatureVersion = models.TextField(null=True, blank=True, verbose_name='SignatureVersion', db_column='SignatureVersion')
    UPN = models.TextField(null=True, blank=True, verbose_name='UPN', db_column='UPN')
    UserEmail = models.TextField(null=True, blank=True, verbose_name='UserEmail', db_column='UserEmail')
    UserName = models.TextField(null=True, blank=True, verbose_name='UserName', db_column='UserName')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastFullScanDateTime', 'LastQuickScanDateTime', 'LastReportedDateTime']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSASECAntivirus(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_Name = models.TextField(null=True, blank=True, verbose_name='Device_Name', db_column='Device_Name')
    Device_Category = models.TextField(null=True, blank=True, verbose_name='Device_Category', db_column='Device_Category')
    Device_Type = models.TextField(null=True, blank=True, verbose_name='Device_Type', db_column='Device_Type')
    Device_Subtype = models.TextField(null=True, blank=True, verbose_name='Device_Subtype', db_column='Device_Subtype')
    Discovery_sources = models.TextField(null=True, blank=True, verbose_name='Discovery_sources', db_column='Discovery_sources')
    Domain = models.TextField(null=True, blank=True, verbose_name='Domain', db_column='Domain')
    AAD_Device_Id = models.TextField(null=True, blank=True, verbose_name='AAD_Device_Id', db_column='AAD_Device_Id')
    First_Seen = models.BigIntegerField(null=True, blank=True, verbose_name='First_Seen', db_column='First_Seen')
    Last_device_update = models.BigIntegerField(null=True, blank=True, verbose_name='Last_device_update', db_column='Last_device_update')
    OS_Platform = models.TextField(null=True, blank=True, verbose_name='OS_Platform', db_column='OS_Platform')
    OS_Distribution = models.TextField(null=True, blank=True, verbose_name='OS_Distribution', db_column='OS_Distribution')
    OS_Version = models.TextField(null=True, blank=True, verbose_name='OS_Version', db_column='OS_Version')
    OS_Build = models.TextField(null=True, blank=True, verbose_name='OS_Build', db_column='OS_Build')
    Windows_10_Version = models.TextField(null=True, blank=True, verbose_name='Windows_10_Version', db_column='Windows_10_Version')
    Tags = models.TextField(null=True, blank=True, verbose_name='Tags', db_column='Tags')
    Group = models.TextField(null=True, blank=True, verbose_name='Group', db_column='Group')
    Is_AAD_Joined = models.TextField(null=True, blank=True, verbose_name='Is_AAD_Joined', db_column='Is_AAD_Joined')
    Device_IPs = models.TextField(null=True, blank=True, verbose_name='Device_IPs', db_column='Device_IPs')
    Device_MACs = models.TextField(null=True, blank=True, verbose_name='Device_MACs', db_column='Device_MACs')
    Risk_Level = models.TextField(null=True, blank=True, verbose_name='Risk_Level', db_column='Risk_Level')
    Exposure_Level = models.TextField(null=True, blank=True, verbose_name='Exposure_Level', db_column='Exposure_Level')
    Health_Status = models.TextField(null=True, blank=True, verbose_name='Health_Status', db_column='Health_Status')
    Onboarding_Status = models.TextField(null=True, blank=True, verbose_name='Onboarding_Status', db_column='Onboarding_Status')
    Device_Role = models.TextField(null=True, blank=True, verbose_name='Device_Role', db_column='Device_Role')
    Cloud_Platforms = models.TextField(null=True, blank=True, verbose_name='Cloud_Platforms', db_column='Cloud_Platforms')
    Is_Internet_Facing = models.TextField(null=True, blank=True, verbose_name='Is_Internet_Facing', db_column='Is_Internet_Facing')
    Enrollment_Status_Code = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status_Code', db_column='Enrollment_Status_Code')
    Managed_By = models.TextField(null=True, blank=True, verbose_name='Managed_By', db_column='Managed_By')
    Enrollment_Status = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status', db_column='Enrollment_Status')
    Vendor = models.TextField(null=True, blank=True, verbose_name='Vendor', db_column='Vendor')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    Firmware_versions = models.TextField(null=True, blank=True, verbose_name='Firmware_versions', db_column='Firmware_versions')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['First_Seen', 'Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDefenderF(models.Model):
    ID = models.AutoField(primary_key=True)
    Device_ID = models.TextField(null=True, blank=True, verbose_name='Device_ID', db_column='Device_ID')
    Device_Name = models.TextField(null=True, blank=True, verbose_name='Device_Name', db_column='Device_Name')
    Device_Category = models.TextField(null=True, blank=True, verbose_name='Device_Category', db_column='Device_Category')
    Device_Type = models.TextField(null=True, blank=True, verbose_name='Device_Type', db_column='Device_Type')
    Device_Subtype = models.TextField(null=True, blank=True, verbose_name='Device_Subtype', db_column='Device_Subtype')
    Discovery_sources = models.TextField(null=True, blank=True, verbose_name='Discovery_sources', db_column='Discovery_sources')
    Domain = models.TextField(null=True, blank=True, verbose_name='Domain', db_column='Domain')
    AAD_Device_Id = models.TextField(null=True, blank=True, verbose_name='AAD_Device_Id', db_column='AAD_Device_Id')
    First_Seen = models.BigIntegerField(null=True, blank=True, verbose_name='First_Seen', db_column='First_Seen')
    Last_device_update = models.BigIntegerField(null=True, blank=True, verbose_name='Last_device_update', db_column='Last_device_update')
    OS_Platform = models.TextField(null=True, blank=True, verbose_name='OS_Platform', db_column='OS_Platform')
    OS_Distribution = models.TextField(null=True, blank=True, verbose_name='OS_Distribution', db_column='OS_Distribution')
    OS_Version = models.TextField(null=True, blank=True, verbose_name='OS_Version', db_column='OS_Version')
    OS_Build = models.TextField(null=True, blank=True, verbose_name='OS_Build', db_column='OS_Build')
    Windows_10_Version = models.TextField(null=True, blank=True, verbose_name='Windows_10_Version', db_column='Windows_10_Version')
    Tags = models.TextField(null=True, blank=True, verbose_name='Tags', db_column='Tags')
    Group = models.TextField(null=True, blank=True, verbose_name='Group', db_column='Group')
    Is_AAD_Joined = models.TextField(null=True, blank=True, verbose_name='Is_AAD_Joined', db_column='Is_AAD_Joined')
    Device_IPs = models.TextField(null=True, blank=True, verbose_name='Device_IPs', db_column='Device_IPs')
    Device_MACs = models.TextField(null=True, blank=True, verbose_name='Device_MACs', db_column='Device_MACs')
    Risk_Level = models.TextField(null=True, blank=True, verbose_name='Risk_Level', db_column='Risk_Level')
    Exposure_Level = models.TextField(null=True, blank=True, verbose_name='Exposure_Level', db_column='Exposure_Level')
    Health_Status = models.TextField(null=True, blank=True, verbose_name='Health_Status', db_column='Health_Status')
    Onboarding_Status = models.TextField(null=True, blank=True, verbose_name='Onboarding_Status', db_column='Onboarding_Status')
    Device_Role = models.TextField(null=True, blank=True, verbose_name='Device_Role', db_column='Device_Role')
    Cloud_Platforms = models.TextField(null=True, blank=True, verbose_name='Cloud_Platforms', db_column='Cloud_Platforms')
    Is_Internet_Facing = models.TextField(null=True, blank=True, verbose_name='Is_Internet_Facing', db_column='Is_Internet_Facing')
    Enrollment_Status_Code = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status_Code', db_column='Enrollment_Status_Code')
    Managed_By = models.TextField(null=True, blank=True, verbose_name='Managed_By', db_column='Managed_By')
    Enrollment_Status = models.TextField(null=True, blank=True, verbose_name='Enrollment_Status', db_column='Enrollment_Status')
    Vendor = models.TextField(null=True, blank=True, verbose_name='Vendor', db_column='Vendor')
    Model = models.TextField(null=True, blank=True, verbose_name='Model', db_column='Model')
    Firmware_versions = models.TextField(null=True, blank=True, verbose_name='Firmware_versions', db_column='Firmware_versions')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['First_Seen', 'Last_device_update']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSASECAntivirusF(models.Model):
    ID = models.AutoField(primary_key=True)
    DeviceName = models.TextField(null=True, blank=True, verbose_name='DeviceName', db_column='DeviceName')
    DeviceState = models.TextField(null=True, blank=True, verbose_name='DeviceState', db_column='DeviceState')
    DeviceState_loc = models.TextField(null=True, blank=True, verbose_name='DeviceState_loc', db_column='DeviceState_loc')
    _ManagedBy = models.TextField(null=True, blank=True, verbose_name='_ManagedBy', db_column='_ManagedBy')
    _ManagedBy_loc = models.TextField(null=True, blank=True, verbose_name='_ManagedBy_loc', db_column='_ManagedBy_loc')
    AntiMalwareVersion = models.TextField(null=True, blank=True, verbose_name='AntiMalwareVersion', db_column='AntiMalwareVersion')
    CriticalFailure = models.TextField(null=True, blank=True, verbose_name='CriticalFailure', db_column='CriticalFailure')
    ProductStatus = models.TextField(null=True, blank=True, verbose_name='ProductStatus', db_column='ProductStatus')
    TamperProtectionEnabled = models.TextField(null=True, blank=True, verbose_name='TamperProtectionEnabled', db_column='TamperProtectionEnabled')
    IsVirtualMachine = models.TextField(null=True, blank=True, verbose_name='IsVirtualMachine', db_column='IsVirtualMachine')
    IsWDATPSenseRunning = models.TextField(null=True, blank=True, verbose_name='IsWDATPSenseRunning', db_column='IsWDATPSenseRunning')
    WDATPOnboardingState = models.TextField(null=True, blank=True, verbose_name='WDATPOnboardingState', db_column='WDATPOnboardingState')
    EngineVersion = models.TextField(null=True, blank=True, verbose_name='EngineVersion', db_column='EngineVersion')
    FullScanOverdue = models.TextField(null=True, blank=True, verbose_name='FullScanOverdue', db_column='FullScanOverdue')
    FullScanRequired = models.TextField(null=True, blank=True, verbose_name='FullScanRequired', db_column='FullScanRequired')
    LastFullScanDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='LastFullScanDateTime', db_column='LastFullScanDateTime')
    LastQuickScanDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='LastQuickScanDateTime', db_column='LastQuickScanDateTime')
    LastQuickScanSignatureVersion = models.TextField(null=True, blank=True, verbose_name='LastQuickScanSignatureVersion', db_column='LastQuickScanSignatureVersion')
    LastReportedDateTime = models.BigIntegerField(null=True, blank=True, verbose_name='LastReportedDateTime', db_column='LastReportedDateTime')
    MalwareProtectionEnabled = models.TextField(null=True, blank=True, verbose_name='MalwareProtectionEnabled', db_column='MalwareProtectionEnabled')
    NetworkInspectionSystemEnabled = models.TextField(null=True, blank=True, verbose_name='NetworkInspectionSystemEnabled', db_column='NetworkInspectionSystemEnabled')
    PendingFullScan = models.TextField(null=True, blank=True, verbose_name='PendingFullScan', db_column='PendingFullScan')
    PendingManualSteps = models.TextField(null=True, blank=True, verbose_name='PendingManualSteps', db_column='PendingManualSteps')
    PendingOfflineScan = models.TextField(null=True, blank=True, verbose_name='PendingOfflineScan', db_column='PendingOfflineScan')
    PendingReboot = models.TextField(null=True, blank=True, verbose_name='PendingReboot', db_column='PendingReboot')
    QuickScanOverdue = models.TextField(null=True, blank=True, verbose_name='QuickScanOverdue', db_column='QuickScanOverdue')
    RealTimeProtectionEnabled = models.TextField(null=True, blank=True, verbose_name='RealTimeProtectionEnabled', db_column='RealTimeProtectionEnabled')
    RebootRequired = models.TextField(null=True, blank=True, verbose_name='RebootRequired', db_column='RebootRequired')
    SignatureUpdateOverdue = models.TextField(null=True, blank=True, verbose_name='SignatureUpdateOverdue', db_column='SignatureUpdateOverdue')
    SignatureVersion = models.TextField(null=True, blank=True, verbose_name='SignatureVersion', db_column='SignatureVersion')
    UPN = models.TextField(null=True, blank=True, verbose_name='UPN', db_column='UPN')
    UserEmail = models.TextField(null=True, blank=True, verbose_name='UserEmail', db_column='UserEmail')
    UserName = models.TextField(null=True, blank=True, verbose_name='UserName', db_column='UserName')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['LastFullScanDateTime', 'LastQuickScanDateTime', 'LastReportedDateTime']
    integer_fields = []
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class Astealicenseusers(models.Model):
    ID = models.AutoField(primary_key=True)
    last_access = models.TextField(null=True, blank=True, verbose_name='last_access', db_column='last_access')
    is_active = models.TextField(null=True, blank=True, verbose_name='is_active', db_column='is_active')
    person_id = models.TextField(null=True, blank=True, verbose_name='person_id', db_column='person_id')
    email_id = models.TextField(null=True, blank=True, verbose_name='email_id', db_column='email_id')
    count_o = models.IntegerField(null=True, blank=True, verbose_name='count_o', db_column='count_o')
    actgr_id = models.TextField(null=True, blank=True, verbose_name='actgr_id', db_column='actgr_id')
    node_id = models.TextField(null=True, blank=True, verbose_name='node_id', db_column='node_id')
    search_name = models.TextField(null=True, blank=True, verbose_name='search_name', db_column='search_name')
    supervisor_id = models.TextField(null=True, blank=True, verbose_name='supervisor_id', db_column='supervisor_id')
    ap_is_bypass_security = models.TextField(null=True, blank=True, verbose_name='ap_is_bypass_security', db_column='ap_is_bypass_security')
    is_mobile_user = models.IntegerField(null=True, blank=True, verbose_name='is_mobile_user', db_column='is_mobile_user')
    product_id = models.TextField(null=True, blank=True, verbose_name='product_id', db_column='product_id')
    group_id = models.TextField(null=True, blank=True, verbose_name='group_id', db_column='group_id')
    is_background_person = models.TextField(null=True, blank=True, verbose_name='is_background_person', db_column='is_background_person')
    Last_Logged_in = models.BigIntegerField(null=True, blank=True, verbose_name='Last_Logged_in', db_column='Last_Logged_in')
    Last_Logged_in_Text = models.TextField(null=True, blank=True, verbose_name='Last_Logged_in_Text', db_column='Last_Logged_in_Text')
    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    date_fields_to_convert = ['Last_Logged_in']
    integer_fields = ['count_o', 'is_mobile_user']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDELTALicensedvsAntiVirus(models.Model):
    ID = models.AutoField(primary_key=True)
    last_access = models.TextField(null=True, blank=True)
    is_active = models.TextField(null=True, blank=True)
    person_id = models.TextField(null=True, blank=True)
    email_id = models.TextField(null=True, blank=True)
    count_o = models.IntegerField(null=True, blank=True)
    actgr_id = models.TextField(null=True, blank=True)
    node_id = models.TextField(null=True, blank=True)
    search_name = models.TextField(null=True, blank=True)
    supervisor_id = models.TextField(null=True, blank=True)
    ap_is_bypass_security = models.TextField(null=True, blank=True)
    is_mobile_user = models.IntegerField(null=True, blank=True)
    product_id = models.TextField(null=True, blank=True)
    group_id = models.TextField(null=True, blank=True)
    is_background_person = models.TextField(null=True, blank=True)
    Last_Logged_in = models.BigIntegerField(null=True, blank=True)
    Last_Logged_in_Text = models.TextField(null=True, blank=True)
    d_DeviceName = models.TextField(null=True, blank=True)
    d_DeviceState = models.TextField(null=True, blank=True)
    d_DeviceState_loc = models.TextField(null=True, blank=True)
    d_ManagedBy = models.TextField(null=True, blank=True)
    d_ManagedBy_loc = models.TextField(null=True, blank=True)
    d_AntiMalwareVersion = models.TextField(null=True, blank=True)
    d_CriticalFailure = models.TextField(null=True, blank=True)
    d_ProductStatus = models.TextField(null=True, blank=True)
    d_TamperProtectionEnabled = models.TextField(null=True, blank=True)
    d_IsVirtualMachine = models.TextField(null=True, blank=True)
    d_IsWDATPSenseRunning = models.TextField(null=True, blank=True)
    d_WDATPOnboardingState = models.TextField(null=True, blank=True)
    d_EngineVersion = models.TextField(null=True, blank=True)
    d_FullScanOverdue = models.TextField(null=True, blank=True)
    d_FullScanRequired = models.TextField(null=True, blank=True)
    d_LastFullScanDateTime = models.BigIntegerField(null=True, blank=True)
    d_LastQuickScanDateTime = models.BigIntegerField(null=True, blank=True)
    d_LastQuickScanSignatureVersion = models.TextField(null=True, blank=True)
    d_LastReportedDateTime = models.BigIntegerField(null=True, blank=True)
    d_MalwareProtectionEnabled = models.TextField(null=True, blank=True)
    d_NetworkInspectionSystemEnabled = models.TextField(null=True, blank=True)
    d_PendingFullScan = models.TextField(null=True, blank=True)
    d_PendingManualSteps = models.TextField(null=True, blank=True)
    d_PendingOfflineScan = models.TextField(null=True, blank=True)
    d_PendingReboot = models.TextField(null=True, blank=True)
    d_QuickScanOverdue = models.TextField(null=True, blank=True)
    d_RealTimeProtectionEnabled = models.TextField(null=True, blank=True)
    d_RebootRequired = models.TextField(null=True, blank=True)
    d_SignatureUpdateOverdue = models.TextField(null=True, blank=True)
    d_SignatureVersion = models.TextField(null=True, blank=True)
    d_UPN = models.TextField(null=True, blank=True)
    d_UserEmail = models.TextField(null=True, blank=True)
    d_UserName = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 51  # Do not change this value
    date_fields_to_convert = ['d_LastQuickScanDateTime', 'd_LastReportedDateTime', 'Last_Logged_in', 'd_LastFullScanDateTime']
    integer_fields = ['is_mobile_user', 'count_o']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []


class ADSDELTALicensedVsAntiVirusTest(models.Model):
    ID = models.AutoField(primary_key=True)
    last_access = models.TextField(null=True, blank=True)
    is_active = models.TextField(null=True, blank=True)
    person_id = models.TextField(null=True, blank=True)
    email_id = models.TextField(null=True, blank=True)
    count_o = models.IntegerField(null=True, blank=True)
    actgr_id = models.TextField(null=True, blank=True)
    node_id = models.TextField(null=True, blank=True)
    search_name = models.TextField(null=True, blank=True)
    supervisor_id = models.TextField(null=True, blank=True)
    ap_is_bypass_security = models.TextField(null=True, blank=True)
    is_mobile_user = models.IntegerField(null=True, blank=True)
    product_id = models.TextField(null=True, blank=True)
    group_id = models.TextField(null=True, blank=True)
    is_background_person = models.TextField(null=True, blank=True)
    Last_Logged_in = models.BigIntegerField(null=True, blank=True)
    Last_Logged_in_Text = models.TextField(null=True, blank=True)
    d_DeviceName = models.TextField(null=True, blank=True)
    d_DeviceState = models.TextField(null=True, blank=True)
    d_DeviceState_loc = models.TextField(null=True, blank=True)
    d_ManagedBy = models.TextField(null=True, blank=True)
    d_ManagedBy_loc = models.TextField(null=True, blank=True)
    d_AntiMalwareVersion = models.TextField(null=True, blank=True)
    d_CriticalFailure = models.TextField(null=True, blank=True)
    d_ProductStatus = models.TextField(null=True, blank=True)
    d_TamperProtectionEnabled = models.TextField(null=True, blank=True)
    d_IsVirtualMachine = models.TextField(null=True, blank=True)
    d_IsWDATPSenseRunning = models.TextField(null=True, blank=True)
    d_WDATPOnboardingState = models.TextField(null=True, blank=True)
    d_EngineVersion = models.TextField(null=True, blank=True)
    d_FullScanOverdue = models.TextField(null=True, blank=True)
    d_FullScanRequired = models.TextField(null=True, blank=True)
    d_LastFullScanDateTime = models.BigIntegerField(null=True, blank=True)
    d_LastQuickScanDateTime = models.BigIntegerField(null=True, blank=True)
    d_LastQuickScanSignatureVersion = models.TextField(null=True, blank=True)
    d_LastReportedDateTime = models.BigIntegerField(null=True, blank=True)
    d_MalwareProtectionEnabled = models.TextField(null=True, blank=True)
    d_NetworkInspectionSystemEnabled = models.TextField(null=True, blank=True)
    d_PendingFullScan = models.TextField(null=True, blank=True)
    d_PendingManualSteps = models.TextField(null=True, blank=True)
    d_PendingOfflineScan = models.TextField(null=True, blank=True)
    d_PendingReboot = models.TextField(null=True, blank=True)
    d_QuickScanOverdue = models.TextField(null=True, blank=True)
    d_RealTimeProtectionEnabled = models.TextField(null=True, blank=True)
    d_RebootRequired = models.TextField(null=True, blank=True)
    d_SignatureUpdateOverdue = models.TextField(null=True, blank=True)
    d_SignatureVersion = models.TextField(null=True, blank=True)
    d_UPN = models.TextField(null=True, blank=True)
    d_UserEmail = models.TextField(null=True, blank=True)
    d_UserName = models.TextField(null=True, blank=True)

    both = models.IntegerField(null=True, blank=True)
    base = models.IntegerField(null=True, blank=True)
    delta = models.IntegerField(null=True, blank=True)

    loader_instance = models.IntegerField(null=True, blank=True)
    json_data = models.JSONField(null=True, blank=True)
    hash_data = models.TextField(null=True, blank=True)

    join_model_instance = 52  # Do not change this value
    date_fields_to_convert = ['d_LastQuickScanDateTime', 'Last_Logged_in', 'd_LastFullScanDateTime', 'd_LastReportedDateTime']
    integer_fields = ['count_o', 'is_mobile_user']
    float_fields = []
    encrypted_fields = []
    unix_dates = []
    ad_unix_dates = []
