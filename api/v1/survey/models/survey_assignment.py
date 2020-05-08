# table header
# Module : S&M | Sub-Module : Survey
# table type : Transaction (Local)
# table name : 2.3.2 Survey Assignment Table
# table description : A transaction table to store vendor assignment for given survey
# frequency of data changes : high
# sample tale data : "Vendor1(id)"
# Reference Table :
# author : Saloni Monde
# created on : 23/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Survey assignment table start

class SurveyAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    survey_id = models.BigIntegerField(null=False, blank=False)
    vendor_id = models.BigIntegerField(null=False, blank=False)
    assigned_date = models.DateField(null=True, blank=True, default=datetime.now())
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.vendor

    def __unicode__(self):
        return self.vendor

def get_survey_assignment_by_id_string(id_string):
    return SurveyAssignment.objects.filter(tenant__id_string = id_string)

def get_survey_assignment_by_tenant_id_string(id_string):
    return SurveyAssignment.objects.get(id_string = id_string)

def get_survey_assignment_by_id(id):
    return SurveyAssignment.objects.get(id = id)

# Create Survey assignment table end
