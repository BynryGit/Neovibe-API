# table header
# module: S&M | sub-module - Campaign
# table type : Master (Local)
# table name : 2.3.6 advertisements master
# table description : A master table to store advertisements in given campaign
# frequency of data changes : high
# sample tale data : campaign = 'Smart360", Ads1 = "Smart360-Awareness-Gas" , Ads2 = "Smart360-Awareness-Power"
# author : Priyanka Kachare
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid
from django.db import models
# Create advertisement master table starts

class Advertisements(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True,on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True,on_delete=models.SET_NULL)
    campaign_id = models.BigIntegerField(default=1, null=True, blank=True)
    group_id = models.BigIntegerField(default=1, null=True, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    objective_id = models.BigIntegerField(default=1, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    frequency_id = models.BigIntegerField(default=1, null=True, blank=True)
    type_id = models.BigIntegerField(default=1, null=True, blank=True)
    potential_consumers = models.BigIntegerField(default=0, null=True, blank=True)
    actual_consumers = models.BigIntegerField(default=0, null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create advertisement master table ends