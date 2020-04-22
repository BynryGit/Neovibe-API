import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.23 Bill Cycle
# Description : It is a lookup table that stores the bill cycles for all the cities to be used in various tables. Bill Cycle and ID of Bill Cycle to be used by Operator or Utility.
# Frequency of data changes : Medium
# Reference Table : 2.3.1. Consumer Master, 2.3.9 Invoice/Bill, 2.3.8.3 Jobcard, 2.3.8.4 Meter Reading, 2.3.8.1 Schedule, 2.3.8.2 Reading Consumer Master, Smart Meter Reading, Smart Meter Billing,
# Auther : Jayshree
# Creation Date : 21-04-2020




class BillCycle(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    bill_cycle_code = models.IntegerField(max_length=200, blank=False, null=False)
    bill_cycle_name = models.CharField(max_length=300, blank=False, null=False)
    bill_cycle_type_id = models.IntegerField(blank=False, null=False)
    area_id = models.IntegerField(blank=False, null=False)
    subarea_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.bill_cycle_name

    def __unicode__(self):
        return self.bill_cycle_name
