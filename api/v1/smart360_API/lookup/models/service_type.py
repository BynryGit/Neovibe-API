# Table Header : Service Type
# Table Type : Lookup (Local)
# Table Name : 2.12.73 Service Type
# Description : Service type and ID of Service type to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : Installation, Convertion, Repair, Maintenance, Outage, Emergency, Meter Reading.
# Reference Table : 2.6.2 SOP Master
# Auther : Jayshree
# Creation Date : 22/04/2020

import datetime
import uuid
from django.db import models

# Start the Code
class ServiceType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_type = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.service_type

    def __unicode__(self):
        return self.service_type

def get_service_type_by_id_string(id_string):
    return ServiceType.objects.get(id_string = id_string)
# End the Code