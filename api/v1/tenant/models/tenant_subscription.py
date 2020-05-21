# table header
# module: Tenant | sub-module - All
# table type : Master
# table name : 1.2  Tenant Subscription
# table description :  It will contain details for Tenant subscription related to tenant subscription id, plan.
# frequency of data changes : Medium
# sample tale data :"sub1234","Plan12"
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


# Create Tenant Subscription table start.

class TenantSubscription(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    subscription_plan_id = models.BigIntegerField(null=True, blank=True)
    subscription_frequency_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    end_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    validity_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.subscription_id

    def __unicode__(self):
        return self.subscription_id

# Create Tenant Subscription table end.
def get_subscription_by_id(id):
    try:
        return TenantSubscription.objects.get(id = id)
    except:
        return False


def get_subscription_by_id_string(id_string):
    try:
        return TenantSubscription.objects.get(id_string = id_string)
    except:
        return False
def get_subscription_by_tenant_id_string(id_string):
    return TenantSubscription.objects.filter(tenant_id_string=id_string)
