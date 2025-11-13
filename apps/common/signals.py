from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.common.models import AuditTrail
from apps.users.middleware import AuditUserMiddleware
from django.utils.functional import SimpleLazyObject

LOCAL_APPS = ['common']

@receiver(pre_save)
def log_model_changes(sender, instance, **kwargs):
    if sender == AuditTrail:
        return

    app_label = sender._meta.app_label
    if app_label not in LOCAL_APPS:
        return
    
    current_user = AuditUserMiddleware.get_current_user()
    if isinstance(current_user, SimpleLazyObject) and current_user.is_anonymous:
        current_user = None

    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)

        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name)
            new_value = getattr(instance, field_name)

            if old_value != new_value:
                audit_trail = AuditTrail.objects.create(
                    content_type=ContentType.objects.get_for_model(instance),
                    object_id=instance.pk,
                    field_name=field_name,
                    old_value=str(old_value),
                    new_value=str(new_value),
                )
                if current_user:
                    audit_trail.changed_by = current_user
                    audit_trail.save()




# @receiver(post_save)
# def log_model_creation(sender, instance, created, **kwargs):
#     if sender == AuditTrail:
#         return

#     app_label = sender._meta.app_label
#     if app_label not in LOCAL_APPS:
#         return

#     current_user = AuditUserMiddleware.get_current_user()
#     if isinstance(current_user, SimpleLazyObject) and current_user.is_anonymous:
#         current_user = None

#     if created:
#         for field in instance._meta.fields:
#             field_name = field.name
#             new_value = getattr(instance, field_name)

#             audit_trail = AuditTrail.objects.create(
#                 content_type=ContentType.objects.get_for_model(instance),
#                 object_id=instance.pk,
#                 field_name=field_name,
#                 old_value=None,
#                 new_value=str(new_value)
#             )
#             if current_user:
#                 audit_trail.changed_by = current_user
#                 audit_trail.save()