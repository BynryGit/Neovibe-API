# table header
# module: Utility | sub-module - Utility Service
# table type : Master
# table name : 2.2.3  Utility Service Plan Rate
# table description :  It will contain details for Utility Service Plan Rate
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

# Create Utility Service Plan Rate table start.
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class UtilityServicePlanRate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_service_plan_id = models.BigIntegerField(null=True, blank=True)
    max_unit_range = models.BigIntegerField(null=True, blank=True)
    unit_id = models.FloatField(null=True, blank=True)
    base_rate = models.FloatField(null=True, blank=True)
    is_taxable = models.BooleanField(default=False)
    taxrate = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.base_rate

    def __unicode__(self):
        return self.base_rate

# Create Utility Service Plan Rate  table end.


def get_utility_service_plans_rates():
    try:
        return UtilityServicePlanRate.objects.all()
    except:
        return False