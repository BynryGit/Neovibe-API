# Table Header : MRU
# Table Type : Lookup (Global)
# Table Name : 2.12.24 MRU
# Description : MRU and ID of MRU to be used by Operator or Utility
# Frequency of data changes : High
# Sample Table Data :
# Reference Table : 2.3.1. Consumer Master
# Auther : Jayshree
# Creation Date : 21-04-2020
import datetime
import uuid
from django.db import models

# Start the Code
class MRU(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    mru_code = models.IntegerField(max_length=200, blank=False, null=False)
    mru = models.CharField(max_length=300, blank=False, null=False)
    area_id = models.IntegerField(blank=False, null=False)
    subarea_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.mru

    def __unicode__(self):
        return self.mru
# End the Code