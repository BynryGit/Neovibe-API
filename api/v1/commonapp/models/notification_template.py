import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class NotificationTemplate(models.Model):
    CHOICES = (
        (0, 'EMAIL'),
        (1, 'SMS'),
        (2, 'WHATSAPP'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    notification_type = models.BigIntegerField(max_length=30, choices=CHOICES, default=0)
    is_template = models.BooleanField(default=False)
    template = models.TextField(max_length=10000, null=True, blank=True)
    is_attachment = models.BooleanField(default=False)
    attachment = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.utility.name

    def __unicode__(self):
        return self.utility.name

def get_notification_template_by_id(id):
    try:
        return NotificationTemplate.objects.get(id = id)
    except Exception as e:
        return False