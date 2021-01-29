import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.notification_type import get_notification_type_by_id


class NotificationSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=1000, blank=True, null=True)
    notification_type_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_notification_type(self):
        notification_type = get_notification_type_by_id(self.notification_type_id)
        return notification_type


def get_notification_subtype_by_id_string(id_string):
    try:
        return NotificationSubType.objects.get(id_string=id_string)
    except:
        return False


def get_notification_subtype_by_id(id):
    try:
        return NotificationSubType.objects.get(id=id)
    except:
        return False