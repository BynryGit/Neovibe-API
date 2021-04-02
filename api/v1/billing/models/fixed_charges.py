# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Meter Fixed Charges
# table description : A lookup table for Meter Fixed Charges of given rate.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Rate Table
# author : Priyanka 
# created on : 02/04/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from v1.utility.models.utility_product import get_utility_product_by_id
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
# Create FixedCharges table start.

class FixedCharges(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    meter_no = models.BigIntegerField(null=True, blank=True)
    weight = models.CharField(max_length=200, null=True, blank=True)
    charges = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.meter_no) +" - "+ str(self.id_string)

    def __unicode__(self):
        return self.meter_no

    @property
    def get_utility_product_name(self):
        try:
            return get_utility_product_by_id(self.utility_product_id)
        except:
            return False
    


# Create FixedCharges table end.

def get_fixed_charges_by_tenant_id_string(tenant_id_string):
    return FixedCharges.objects.filter(tenant__id_string=tenant_id_string)

def get_fixed_charges_by_id_string(id_string):
    try:
        return FixedCharges.objects.get(id_string = id_string)
    except:
        return False

def get_fixed_charges_by_id_meter_no(meter_no):
    try:
        return FixedCharges.objects.get(meter_no = meter_no).charges
    except:
        return 0
