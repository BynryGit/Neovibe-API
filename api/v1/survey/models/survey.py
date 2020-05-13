# table header
# Module : S&M | Sub-Module : Survey
# table type : Master (Local)
# table name : 2.3.1 Survey master Table
# table description : A Master table that store survey details
# frequency of data changes : high
# sample tale data : "Domestic consumer survey", "New Location Survey"
# Reference Table : 2.3.2 Survey Assignment Table, 2.3.3 Survey Transaction Table , 2.3.4 Survey Consumer Table
# Author : Saloni Monde
# created on : 23/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

from v1.survey.models.survey_objective import get_survey_objective_by_id
from v1.survey.models.survey_type import get_survey_type_by_id
from v1.survey.models.survey_status import get_survey_status_by_id


# Create Survey table start

class Survey(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True, blank=True)
    objective_id = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    type_id = models.BigIntegerField(null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    no_of_consumers = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_objective(self):
        objective = get_survey_objective_by_id(self.objective_id)
        return objective

    @property
    def get_type(self):
        type = get_survey_type_by_id(self.type_id)
        return type

    @property
    def get_status(self):
        status = get_survey_status_by_id(self.status_id)
        return status

def get_survey_by_tenant_id_string(id_string):
    return Survey.objects.filter(tenant__id_string = id_string)

def get_survey_by_id_string(id_string):
    try:
        return Survey.objects.get(id_string = id_string)
    except:
        return False

def get_survey_by_id(id):
    try:
        return Survey.objects.get(id = id)
    except:
        return False

# Create Survey table end
