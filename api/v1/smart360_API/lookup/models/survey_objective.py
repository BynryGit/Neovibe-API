# table header
# table type : lookup (Local)
# table name : 2.12.31 Objective (Survey)
# table description : A lookup table for for objectives for given campaign.
# frequency of data changes : Medium
# sample tale data : "Update consumer data"
# reference tables : 2.3.1 Survey master Table
# author : Saloni
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Survey Objective table start.

class SurveyObjective(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    objective = models.CharField(max_length=500, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.objective

# Create Survey Objective table end.

