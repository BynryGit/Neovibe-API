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
from django.db import models  # importing package for database
import fsm
from django.contrib.postgres.fields import JSONField

# *********** TENANT PLAN STATUS CONSTANTS **************
TENANT_PLAN_STATUS_DICT = {
    "TRIAL": 0,
    "SUBSCRIPTION": 1,
    "EXPIRED":2,
    "CANCELLED":3
}


# Create Tenant Subscription Plan table start.

class TenantSubscriptionPlan(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'TRIAL'),
        (1, 'SUBSCRIPTION'),
        (2, 'EXPIRED'),
        (3, 'CANCELLED')
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subscription_name = models.CharField(max_length=200, blank=True, null=True)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    max_storage = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(choices=CHOICES, default=0)
    module_obj = JSONField(default='')
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.subscription_name

    def __unicode__(self):
        return self.subscription_name

# Create Tenant Subscription Plan table end.


def get_tenant_subscription_plan_by_id(id):
    try:
        return TenantSubscriptionPlan.objects.get(id=id)
    except:
        return False


def get_tenant_subscription_plan_by_id_string(id_string):
    try:
        return TenantSubscriptionPlan.objects.get(id_string=id_string)

    except:
        return False
