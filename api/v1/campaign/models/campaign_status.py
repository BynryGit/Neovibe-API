import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Campaign Status table start.

class CampaignStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

# Create Campaign Status table end.

def get_cam_status_by_tenant_id_string(tenant_id_string):
    return CampaignStatus.objects.filter(tenant__id_string=tenant_id_string)

def get_cam_status_by_id_string(id_string):
    try:
        return CampaignStatus.objects.get(id_string = id_string)
    except:
        return False

def get_cam_status_by_id(id):
    return CampaignStatus.objects.get(id = id)