# table header
# module: Sourcing, Purchase
# table type : Master
# table name : Supplier
# table description : The Supplier Master table saves the basic details of any Supplier that exists.
# frequency of data changes : High
# sample table data : "Supplier 1", "Supplier 2"
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.tenant.models.tenant_city import get_tenant_city_by_id
from v1.tenant.models.tenant_country import get_tenant_country_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_state import get_tenant_state_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Supplier Master table start

class Supplier(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    country_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    source = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.BigIntegerField(blank=True, null=True)
    status_id = models.BigIntegerField(blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_tenant_country(self):
        country = get_tenant_country_by_id(self.country_id)
        return country

    @property
    def get_tenant_state(self):
        state = get_tenant_state_by_id(self.state_id)
        return state

    @property
    def get_tenant_city(self):
        city = get_tenant_city_by_id(self.city_id)
        return city

# Create Supplier Master table end.


def get_supplier_by_tenant_id_string(id_string):
    return Supplier.objects.filter(tenant__id_string = id_string)

def get_supplier_by_id_string(id_string):
    try:
        return Supplier.objects.get(id_string = id_string)
    except:
        return False

def get_supplier_by_id(id):
    try:
        return Supplier.objects.get(id = id)
    except:
        return False

