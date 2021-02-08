import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField
# Create Integration Type table start
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.integration_type import get_integration_type_by_id
from v1.commonapp.models.integration_subtype import get_integration_sub_type_by_id
from v1.utility.models.utility_module import get_utility_module_by_id


class IntegrationMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    integration_type_id = models.BigIntegerField(null=True, blank=True)
    integration_sub_type_id = models.BigIntegerField(null=True, blank=True)
    module_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    request_parameters = JSONField()
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
    def get_integration_type(self):
        return get_integration_type_by_id(self.integration_type_id)

    @property
    def get_integration_sub_type(self):
        return get_integration_sub_type_by_id(self.integration_sub_type_id)

    @property
    def get_utility_module(self):
        return get_utility_module_by_id(self.module_id)


def get_integration_master_by_id_string(id_string):
    try:
        return IntegrationMaster.objects.get(id_string=id_string)
    except:
        return False


def get_integration_master_by_id(id):
    try:
        return IntegrationMaster.objects.get(id=id)
    except:
        return False
