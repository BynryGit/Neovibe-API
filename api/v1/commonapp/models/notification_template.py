import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.commonapp.models.sub_module import get_sub_module_by_id
from django.utils import timezone # importing package for datetime

# from v1.utility.models.utility_master import UtilityMaster


class NotificationTemplate(models.Model):
    CHOICES = (
        (0, 'EMAIL'),
        (1, 'SMS'),
        (2, 'WHATSAPP'),
        (3, 'IN APP NOTIFICATIONS')
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey('utility.UtilityMaster', blank=True, null=True, on_delete=models.SET_NULL)
    notification_type = models.BigIntegerField(choices=CHOICES, default=0)
    is_template = models.BooleanField(default=True)
    template = models.TextField(max_length=100000, null=True, blank=True)
    is_attachment = models.BooleanField(default=False)
    attachment = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.utility.name

    def __unicode__(self):
        return self.utility.name

    @property
    def get_sub_module(self):
        sub_module = get_sub_module_by_id(self.sub_module_id)
        return sub_module


def get_notification_template_by_id(id):
    try:
        return NotificationTemplate.objects.get(id=id)
    except Exception as e:
        return False


def get_notification_template_by_id_string(id_string):
    try:
        return NotificationTemplate.objects.get(id_string=id_string)
    except Exception as e:
        return False
