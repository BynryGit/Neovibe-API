# table header
# module: Tenant | sub-module - All
# table type : Master - Global
# table name : 1.1 Tenant Master
# table description : It is Tenant Master table. It will contain details for Tenant
# frequency of data changes : Medium
# sample table data : MNGL, VGL, SGL
# reference tables :-
# author : Gauri Deshmukh
# created on : 24/04/2020
# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_city import get_tenant_city_by_id
from v1.tenant.models.tenant_country import get_tenant_country_by_id
from v1.tenant.models.tenant_state import get_tenant_state_by_id
from v1.tenant.models.tenant_status import get_tenant_status_by_id
from django.utils import timezone # importing package for datetime

# Create Tenant Master table start.


class TenantMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    short_name = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    mobile_no = models.CharField(max_length=200, blank=True, null=True)
    tenant_city_id = models.BigIntegerField(null=True, blank=True)
    tenant_country_id = models.BigIntegerField(null=True, blank=True)
    tenant_currency_id = models.BigIntegerField(null=True, blank=True)
    tenant_state_id = models.BigIntegerField(null=True, blank=True)
    tenant_region_id = models.BigIntegerField(null=True, blank=True)
    pan_no = models.CharField(max_length=200, blank=True, null=True)
    tax_id = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    short_logo = models.CharField(max_length=200, blank=True, null=True)
    long_logo = models.CharField(max_length=200, blank=True, null=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return self.name

    @property
    def get_tenant_country(self):
        country = get_tenant_country_by_id(self.tenant_country_id)
        return country

    @property
    def get_tenant_state(self):
        state = get_tenant_state_by_id(self.tenant_state_id)
        return state

    @property
    def get_tenant_city(self):
        city = get_tenant_city_by_id(self.tenant_city_id)
        return city

    @property
    def get_tenant_status(self):
        status = get_tenant_status_by_id(self.status_id)
        return status

# Create Tenant Master table end.


def get_tenant_by_id(id):
    try:
        return TenantMaster.objects.get(id=id, is_active=True)
    except:
        return False


def get_tenant_by_id_string(id_string):
    try:
        return TenantMaster.objects.get(id_string=id_string, is_active=True)
    except:
        return False

