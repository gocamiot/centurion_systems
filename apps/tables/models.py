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


