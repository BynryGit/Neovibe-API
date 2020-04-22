import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.9 Sub-Area
# Description : This table will store sub area with respect to area.
# Frequency of data changes : Low
# Reference Table : 2.3.1 Survey Table, 2.3.4 Survey Consumer Table, 2.3.8 Campaign Transaction Table, 2.3.2. Consumer - Registration, Service Assignment, Service AppoIntegerFieldment, 2.7.1. Employee
# Auther : Jayshree
# Creation Date : 21-04-2020



class SubArea(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    sub_area_name = models.CharField(max_length=30, blank=False, null=False)
    area_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_area_name

    def __unicode__(self):
        return self.sub_area_name
