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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Survey table start

class Survey(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    objective = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    category = models.IntegerField(null=True, blank=True)
    sub_category = models.IntegerField(null=True, blank=True)
    no_of_consumers = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now())
    end_date = models.DateField(null=True, blank=True, default=datetime.now())
    area = models.IntegerField(null=True, blank=True)
    sub_area = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Survey table end
