__author__ = "aki"

# table header
# module: Utility | sub-module - Utility Usage
# table type : Transactional
# table name :2.3  Utility Usage Summary
# table description : It will contain summary of usage by the utility.
# frequency of data changes : High
# sample tale data :"1200","2324","May","5GB"
# reference tables : 2.1. UtilityMaster
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Utility usage summary table start.

class UtilityUsageSummary(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    no_of_users = models.BigIntegerField(null=True, blank=True)
    no_of_consumers = models.BigIntegerField(null=True, blank=True)
    total_no_of_transaction = models.BigIntegerField(null=True, blank=True)
    no_of_cities = models.BigIntegerField(null=True, blank=True)
    no_of_documents = models.BigIntegerField(null=True, blank=True)
    total_storage_in_use = models.FloatField(null=True, blank=True)
    month = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.month

    def __unicode__(self):
        return self.month

# Create Utility Usage Summary table end.


def get_utility_usage_summary_by_id(id):
    try:
        return UtilityUsageSummary.objects.get(id = id)
    except:
        return False


def get_utility_usage_summary_by_id_string(id_string):
    try:
        return UtilityUsageSummary.objects.get(id_string = id_string)
    except:
        return False


def get_utility_usage_summary_by_utility_id_string(id_string):
    try:
        return UtilityUsageSummary.objects.get(utility__id_string = id_string)
    except:
        return False
