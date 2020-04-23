# table header
# table type : Master (Local)
# table name : 2.3.6 Campaign Master
# table description : A Master table that store campaign details
# frequency of data changes : high
# sample tale data : "Smart360" , "Awareness"
# author : Priyanka
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import datetime
import uuid
from django.db import models

# Create Campaign Master table start

class CampaignMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    cam_group_id = models.CharField(null=True, blank=True)
    name = models.CharField(max_length=200,null=False, blank=False)
    objective_id = models.IntegerField(default=1,null=True, blank=True)
    description = models.TextField(max_length=1000,null=True, blank=True)
    frequency_id = models.IntegerField(default=1, null=True, blank=True)
    type_id = models.IntegerField(default=1, null=True, blank=True)
    potential_consumers = models.IntegerField(default=0, null=True, blank=True)
    actual_consumers = models.IntegerField(default=0, null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    sub_category_id = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    area_id = models.IntegerField(null=True, blank=True)
    sub_area_id = models.IntegerField(null=True, blank=True)
    status_id = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    updated_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    created_by = models.ForeignKey(User, null=False, blank=False)
    updated_by = models.ForeignKey(User, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # Create Campaign Master table ends