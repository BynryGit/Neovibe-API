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
from v1.survey.models.survey_type import get_survey_type_by_id
from v1.survey.models.survey_subtype import get_survey_subtype_by_id


# Create Survey Objective table start.

class SurveyObjective(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    objective = models.CharField(max_length=500, blank=False, null=False)
    survey_type_id = models.BigIntegerField(null=True, blank=True)
    survey_subtype_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.objective

    def __unicode__(self):
        return self.objective
    
    @property
    def get_survey_type(self):
        survey_type = get_survey_type_by_id(self.survey_type_id)
        return survey_type

    @property
    def get_survey_subtype(self):
        survey_subtype = get_survey_subtype_by_id(self.survey_subtype_id)
        return survey_subtype

def get_survey_objective_by_tenant_id_string(id_string):
    return SurveyObjective.objects.filter(tenant__id_string = id_string)

def get_survey_objective_by_id_string(id_string):
    return SurveyObjective.objects.get(id_string = id_string)

def get_survey_objective_by_id(id):
    return SurveyObjective.objects.get(id = id)

# Create Survey Objective table end.

