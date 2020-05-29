# table header
# module: Tenant | sub-module - Tenant Subscription
# table type : Master
# table name : 1.2  Tenant Subscription Plan
# table description :  It will contain details for Tenant subscription Plan
# frequency of data changes : Medium
# sample tale data : "Plan - A"
# reference tables : 1.1 Tenant Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tenant Subscription Plan table start.

class TenantSubscriptionPlan(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscription_id = models.BigIntegerField(null=True, blank=True)
    subscription_plan_id = models.BigIntegerField(null=True, blank=True)
    subscription_type = models.CharField(max_length=200, blank=True, null=True)
    subscription_name = models.CharField(max_length=200, blank=True, null=True)
    subscription_frequency_id = models.BigIntegerField(null=True, blank=True)
    short_name = models.BigIntegerField(null=True, blank=True)

    description = models.CharField(max_length=500, blank=True, null=True)
    max_utility  = models.BigIntegerField(null=True, blank=True)
    max_user = models.BigIntegerField(null=True, blank=True)
    max_consumer = models.BigIntegerField(null=True, blank=True)
    max_storage = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.subscription_name

    def __unicode__(self):
        return self.subscription_name

# Create Tenant Subscription Plan table end.

def get_subscription_plan_by_id(id):
    try:
        return TenantSubscriptionPlan.objects.get(id = id)
    except:
        return False


def get_subscription_plan_by_id_string(id_string):
    try:
        return TenantSubscriptionPlan.objects.get(id_string = id_string)

    except:
        return False

def get_subscription_plan_by_tenant_id_string(id_string):
    return TenantSubscriptionPlan.objects.filter(tenant_id_string=id_string)
