# table header
# table type : Master
# table name : 1.8 Tenant Summary on Monthly Basis
# table description :  It will contain details for Tenant's summary  with respect to his monthly usage.
# frequency of data changes : High
# sample tale data :
# reference tables : 1.1 Tenant Master,
# author : Gauri Deshmukh
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Tenant Summary on Monthly Basis table start.

class TenantSummaryOnMonthlyBasis(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    no_of_utilities = models.IntegerField(null=True, blank=True)
    no_of_users = models.IntegerField(null=True, blank=True)
    no_of_consumers = models.IntegerField(null=True, blank=True)
    total_no_of_transaction = models.IntegerField(null=True, blank=True)
    no_of_cities = models.IntegerField(null=True, blank=True)
    no_of_documents = models.IntegerField(null=True, blank=True)
    total_storage_in_use = models.FloatField(null=True, blank=True)
    month = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id_string

    def __unicode__(self):
        return self.id_string

# Create Tenant Summary on Monthly Basis table end.
