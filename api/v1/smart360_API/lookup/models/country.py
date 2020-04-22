import datetime
import uuid

from django.db import models

# Table Type : Lookup
# Table Name : 2.12.5 Country
# Description : Country and ID of Country to be used by Operator or Utility
# Frequency of data changes : Low
# Reference Table : 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.7. Branch details, 2.5.3. Vendor Details
# Auther : Jayshree
# Creation Date : 21-04-2020

class Country(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    country = models.CharField(max_length=20, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.country

    def __unicode__(self):
        return self.country
