# table header
# module: Tenant | sub-module - All
# table type : Master
# table name : 1.8 Tenant Summary on Monthly Basis
# table description :  It will contain details for Tenant's summary  with respect to his monthly usage.
# frequency of data changes : High
# sample tale data :
# reference tables : 1.1 Tenant Master,
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database


# Create Tenant Summary on Monthly Basis table start.

class TenantSummaryOnMonthlyBasis(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    no_of_utilities = models.BigIntegerField(null=True, blank=True)
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
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id_string

    def __unicode__(self):
        return self.id_string


# Create Tenant Summary on Monthly Basis table end.


def get_tenant_usage_summary_by_id(id):
    try:
        return TenantSummaryOnMonthlyBasis.objects.get(id = id)
    except:
        return False


def get_tenant_usage_summary_by_id_string(id_string):
    try:
        return TenantSummaryOnMonthlyBasis.objects.get(id_string = id_string)
    except:
        return False


def get_tenant_usage_summary_by_tenant_id_string(id_string):
    try:
        return TenantSummaryOnMonthlyBasis.objects.get(tenant__id_string = id_string)
    except:
        return False