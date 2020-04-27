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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant Subscription table start.

class TenantSubscription(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    subscription_id = models.IntegerField(null=True, blank=True)
    subscription_frequency_id = models.IntegerField(null=True, blank=True) #Payment fr
    subscription_plan_id = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    validity_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.subscription_id

    def __unicode__(self):
        return self.subscription_id

# Create Tenant Subscription table end.
