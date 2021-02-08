import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database

# Create Integration Sub Type table start
from v1.utility.models.utility_master import UtilityMaster


class IntegrationSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Integration Sub Type table end


def get_integration_sub_type_by_id_string(id_string):
    try:
        return IntegrationSubType.objects.get(id_string=id_string)
    except:
        return False


def get_integration_sub_type_by_id(id):
    return IntegrationSubType.objects.get(id=id)


def get_integration_sub_type_by_name(name):
    try:
        return IntegrationSubType.objects.get(name=name)
    except:
        return False