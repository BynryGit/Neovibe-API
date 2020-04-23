# Table Header : Frequency
# Table Type : Lookup (Global)
# Table Name : 2.12.25 Frequency
# Description : It captures Frequency and ID of various Frequency to be used by Operator or Utility
# Sample Table Data: 1 month, 2 month;
# Frequency of data changes : Low
# Reference Table : 2.3.8 Campaign Transaction Table, 2.4.6 Asset-SOP details,
# Auther : Jayshree
# Creation Date : 21-04-2020
import datetime
import uuid
from django.db import models

# Start the Code
class Frequency(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    frequency = models.CharField(max_length=300, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.frequency

    def __unicode__(self):
        return self.frequency
# End The code