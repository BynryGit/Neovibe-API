# table header
# module: Utility | sub-module - Service plan
# table type : Master
# table name :2.2.2 Service Plan Rate
# table description : This table contains the details of rates for given service plan.
# frequency of data changes : Low
# sample tale data : "27","29.85"
# reference tables :2.2.1 Utility Service Master
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Service Plan Rate table start.

class  ServicePlanRate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    utility_service_plan_id = models.IntegerField(null=True, blank=True)
    city_id =  models.IntegerField(null=True, blank=True)
    max_unit_range = models.IntegerField(null=True, blank=True)
    unit_id = models.FloatField(null=True, blank=True)
    base_rate = models.FloatField(null=True, blank=True)
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

# Create Service Plan rate table end.
