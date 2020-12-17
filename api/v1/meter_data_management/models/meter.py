import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class Meter(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    meter_make = models.CharField(max_length=200, blank=True, null=True)
    meter_type = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_smart_meter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.meter_make + ' ' + str(self.id_string)

    def __unicode__(self):
        return self.meter_make


def get_meter_by_id_string(id_string):
    try:
        return Meter.objects.get(id_string=id_string)
    except:
        return False


def get_meter_by_id(id):
    try:
        return Meter.objects.get(id=id)
    except:
        return False
