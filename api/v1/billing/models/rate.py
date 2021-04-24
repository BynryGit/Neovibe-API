# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Rate
# table description : A lookup table for Rate of given rate.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Rate Table
# author : Priyanka 
# created on : 01/03/2021

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
# Create Rate table start.

class Rate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    consumer_category_id = models.BigIntegerField(null=True, blank=True)
    consumer_subcategory_id = models.BigIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=200, blank=False, null=False)
    rate = models.CharField(max_length=200, blank=False, null=False)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_fixted_rate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.rate) +" - "+ str(self.id_string)

    def __unicode__(self):
        return self.rate

    @property
    def get_utility_product_name(self):
        try:
            return get_utility_product_by_id(self.utility_product_id)
        except:
            return False
    
    @property
    def get_consumer_category(self):
        try:
            return get_consumer_category_by_id(self.consumer_category_id)
        except:
            return False
    @property
    def get_consumer_sub_category(self):
        try:
            return get_consumer_sub_category_by_id(self.consumer_subcategory_id)
        except:
            return False

# Create Rate table end.

def get_rate_by_tenant_id_string(tenant_id_string):
    return Rate.objects.filter(tenant__id_string=tenant_id_string)

def get_rate_by_id_string(id_string):
    try:
        return Rate.objects.get(id_string = id_string)
    except:
        return False

def get_rate_by_id(id):
    try:
        return Rate.objects.get(id = id)
    except:
        return False

def get_rate_by_category_sub_category_wise(utility,utility_product_id,consumer_category_id,consumer_sub_category_id):
    try:
        print('======',utility,utility_product_id,consumer_category_id,consumer_sub_category_id)
        return Rate.objects.filter(utility=utility,utility_product_id=utility_product_id,consumer_category_id=consumer_category_id,consumer_subcategory_id=consumer_sub_category_id,is_active=True).order_by('id')
    except:
        return False