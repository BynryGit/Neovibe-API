# table header
# module: S&M | sub-module - All
# table type : Master (Local)
# table name : 2.3.6 Campaign Master
# table description : A Master table that store campaign details
# frequency of data changes : high
# sample tale data : "Smart360" , "Awareness"
# author : Priyanka
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid
from django.db import models

from v1.campaign.models.campaign_status import get_cam_status_by_id
from v1.campaign.models.campaign_group import get_camp_group_by_id
from v1.campaign.models.campaign_objective import get_cam_objective_by_id
from v1.commonapp.models.frequency import get_frequency_by_id

# Create Campaign Master table start

class Campaign(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True,on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True,on_delete=models.SET_NULL)
    group_id = models.BigIntegerField(default=1,null=True, blank=True)
    name = models.CharField(max_length=200,null=False, blank=False)
    objective_id = models.BigIntegerField(default=1,null=True, blank=True)
    description = models.TextField(max_length=1000,null=True, blank=True)
    frequency_id = models.BigIntegerField(default=1, null=True, blank=True)
    potential_consumers = models.BigIntegerField(default=0, null=True, blank=True)
    actual_consumers = models.BigIntegerField(default=0, null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    end_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    area_id = models.BigIntegerField(default=1,null=True, blank=True)
    sub_area_id = models.BigIntegerField(default=1,null=True, blank=True)
    status_id = models.BigIntegerField(default=1,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_group(self):
        group = get_camp_group_by_id(self.group_id)
        return group

    @property
    def get_objective(self):
        objective = get_cam_objective_by_id(self.objective_id)
        return objective

    @property
    def get_frequency(self):
        frequency = get_frequency_by_id(self.frequency_id)
        return frequency

    @property
    def get_status(self):
        status = get_cam_status_by_id(self.status_id)
        return status



def get_campaign_by_id_string(id_string):
    try:
        return Campaign.objects.get(id_string=id_string)
    except:
        return False

def get_campaign_by_id(id):
    try:
        return Campaign.objects.get(id=id)
    except:
        return False
    # Create Campaign Master table ends