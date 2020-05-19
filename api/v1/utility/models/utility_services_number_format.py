# table header
# module: Utility | sub-module - Utility Service
# table type : Master
# table name : 2.2.5  Utility Service Number Format
# table description :  It will contain details for Utility Service Number Format
# frequency of data changes : Low
# sample tale data : "Plan - A"
# reference tables : 2.1 Utility Master
# author : Gauri Deshmukh
# created on : 27/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
# Create Utility Service Number Format table start.
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class UtilityServiceNumberFormat(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.CharField(max_length=200, blank=False, null=False) #Survey, Campaign, Registration, Consumer, Receipt, Contract
    is_prefix = models.BooleanField(default=False)
    prefix = models.CharField(max_length=5, blank=True, null=True) #Emp, TEC
    startingno = models.BigIntegerField(null=True, blank=True) #Range as in =0,00001,100001
    currentno = models.BigIntegerField(null=True, blank=True) #Range as in =0,00001,100001
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.item

    def __unicode__(self):
        return self.item

# Create Utility Service Number Format table end.


def get_utility_service_number_format_by_utility_id_string_and_item(id_string, item):
    try:
        return UtilityServiceNumberFormat.objects.get(utility__id_string=id_string, item=item, is_active=True)
    except:
        return False
