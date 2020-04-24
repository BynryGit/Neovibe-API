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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Survey assignment table start

class SurveyAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    survey = models.IntegerField(null=False, blank=False)
    vendor = models.IntegerField(null=False, blank=False)
    assigned_date = models.DateField(null=True, blank=True, default=datetime.now())
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    status = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.vendor

    def __unicode__(self):
        return self.vendor

# Create Survey assignment table end
