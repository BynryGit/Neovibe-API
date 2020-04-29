# table header
# module: S&M  | sub-module - Survey,campaign
# table type : lookup (Local)
# table name : 2.12.31 Objective (Survey)
# table description : A lookup table for objectives for given Survey.
# frequency of data changes : Medium
# sample tale data : "Update consumer data"
# reference tables : 2.3.1 Survey master Table
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Survey Objective table start.

class SurveyObjective(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    objective = models.CharField(max_length=500, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.objective

    def __unicode__(self):
        return self.objective

def get_survey_objective_by_id_string(id_string):
    return SurveyObjective.objects.get(id_string = id_string)

def get_survey_objective_by_id(id):
    return SurveyObjective.objects.get(id = id)

# Create Survey Objective table end.

