# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Bill Cycle
# table description : A lookup table for month of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Bill Cycle Table
# author : Priyanka 
# created on : 01/03/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.zone import get_zone_by_id
from v1.commonapp.models.division import get_division_by_id
from v1.commonapp.models.area import get_area_by_id
from django.contrib.postgres.fields import JSONField

# Create Bill Cycle table start.

class BillCycle(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(null=True, blank=True)
    zone_id = models.BigIntegerField(null=True, blank=True)
    division_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    subarea_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    bill_cycle_code = models.CharField(max_length=200, blank=False, null=False)
    bill_cycle_name = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.bill_cycle_name

    def __unicode__(self):
        return self.bill_cycle_name

    @property
    def get_city(self):
        city = get_city_by_id(self.city_id)
        return city

    @property
    def get_zone(self):
        zone = get_zone_by_id(self.zone_id)
        return zone

    @property
    def get_division(self):
        division = get_division_by_id(self.division_id)
        return division

    @property
    def get_area(self):
        area = get_area_by_id(self.area_id)
        return area


# Create Bill Cycle table end.

def get_bill_cycle_by_tenant_id_string(tenant_id_string):
    return BillCycle.objects.filter(tenant__id_string=tenant_id_string)

def get_bill_cycle_by_id_string(id_string):
    try:
        return BillCycle.objects.get(id_string = id_string)
    except:
        return False

def get_bill_cycle_by_id(id):
    try:
        return BillCycle.objects.get(id = id)
    except:
        return False