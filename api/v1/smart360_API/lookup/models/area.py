# table header : Area
# Table Type : Lookup (Global)
# Table Name : 2.12.8 Area
# Description : It captures area and ID of various Area to be used by Operator or Utility
# Frequency of data changes : Low
# Sample table : "Shivajinagar", "Kothrod".
# Reference Table : 2.3.1 Survey Table, 2.3.4 Survey Consumer Table, 2.3.8 Campaign Transaction Table,
#                   2.3.2. Consumer - Registration, Service Assignment, Service AppoIntegerFieldment, 2.7.1. Employee
# Auther : Jayshree
# Creation Date : 21/04/2020

import datetime
import uuid
from django.db import models

# Start the Code

class Area(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    area = models.CharField(max_length=30, blank=False, null=False)
    city_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.area

    def __unicode__(self):
        return self.area_name

def get_areas_by_tenant_id_string(id_string):
    return Area.objects.filter(tenant__id_string=id_string)

