import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_service_master import get_service_master_by_id


class UtilityService(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.utility.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.utility.name

    @property
    def get_service(self):
        service = get_service_master_by_id(self.service_id)
        return service


def get_utility_service_by_id_string(id_string):
    try:
        return UtilityService.objects.get(id_string=id_string)
    except:
        return False


def get_utility_service_by_id(id):
    try:
        return UtilityService.objects.get(id=id)
    except:
        return False
