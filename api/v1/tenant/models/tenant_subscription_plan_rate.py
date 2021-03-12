# table header
# module: Tenant | sub-module - Tenant Subscription plan
# table type : Master
# table name : 1.3  Tenant Subscription Plan Rate
# table description :  It will contain details of rate for Tenant subscription Plan
# frequency of data changes : Medium
# sample tale data : "Plan - A"
# reference tables : 1.1 Tenant Master, 1.2. Tenant Subscription Plan
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from django.utils import timezone # importing package for datetime


# Create Tenant Subscription Plan Rate table start.

class TenantSubscriptionPlanRate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    subscription_plan_id = models.BigIntegerField(null=True, blank=True)
    subscription_name = models.CharField(max_length=200, blank=True, null=True)
    tenant_subscription_id = models.BigIntegerField(null=True, blank=True)
    base_rate = models.FloatField(null=True, blank=True)
    currency_id = models.BigIntegerField(null=True, blank=True)
    region_id = models.BigIntegerField(null=True, blank=True)
    country_id = models.BigIntegerField(null=True, blank=True)
    is_taxable = models.BooleanField(default=False)
    tax = models.FloatField(null=True, blank=True)
    effective_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.subscription_name

    def __unicode__(self):
        return self.subscription_name

# Create Tenant Subscription Plan Rate table end.


def get_tenant_subscription_plan_rate_by_id(id):
    try:
        return TenantSubscriptionPlanRate.objects.get(id=id)
    except:
        return False


def get_tenant_subscription_plan_rate_by_id_string(id_string):
    try:
        return TenantSubscriptionPlanRate.objects.get(id_string=id_string)
    except:
        return False
