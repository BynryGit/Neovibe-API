# table header
# module:
# Table Type :
# Table Name : Bill Cycle Reading Allocation
# Description : bill cycle validation assignment
# Frequency of data changes : Medium
# Sample Table Data :
# Reference Table :
# Author : Akshay
# Creation Date : 17/06/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from master.models import User
from v1.meter_reading.models.bill_cycle import BillCycle
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Bill Reading Allocation table start

class BillCycleReadingAllocation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    bill_cycle = models.ForeignKey(BillCycle, blank=False, null=False, on_delete=models.SET_NULL)
    validator_one = models.ForeignKey(User, blank=False, null=False, related_name="validator_one", on_delete=models.SET_NULL)
    validator_two = models.ForeignKey(User, blank=False, null=False, related_name="validator_two", on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.bill_cycle

    def __unicode__(self):
        return self.bill_cycle

# Create Bill Reading Allocation table end


def get_bill_cycle_reading_alloaction_by_id(id):
    try:
        return BillCycleReadingAllocation.objects.get(id=id)
    except:
        return False


def get_bill_cycle_reading_alloaction_by_id_string(id_string):
    try:
        return BillCycleReadingAllocation.objects.get(id_string=id_string)
    except:
        return False
