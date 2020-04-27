# table header
# module: Tenant | sub-module - Tenant Subscription plan
# table type : Master
# table name : 1.3  Tenant Subscription Plan
# table description :  It will contain details of rate for Tenant subscription Plan
# frequency of data changes : Medium
# sample tale data : "Plan - A"
# reference tables : 1.1 Tenant Master, 1.2. Tenant Subscription Plan
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant Subscription Plan Rate table start.

class TenantSubscriptionPlanRate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    base_rate = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=200, blank=False, null=False)
    region = models.CharField(max_length=200, blank=False, null=False)
    country = models.CharField(max_length=200, blank=False, null=False)
    is_taxable = models.BooleanField(default=False)
    tax = models.FloatField(null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.base_rate

    def __unicode__(self):
        return self.base_rate

# Create Tenant Subscription Plan Rate table end.
