__author__ = "priyanka"

# Table Header
# Module: Consumer Care & Ops | Sub-Module :  billing, Bill Distribution
# Table Type : Master
# Table Name : Bill Schedule Log
# Description : It is bill schedule log table. This table will save all the bill schedules log.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Priyanka 
# Creation Date : 08/03/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.billing.models.bill_schedule import get_schedule_bill_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_product import get_utility_product_by_id


# Create Schedule Table Start


class ScheduleBillLog(models.Model):
    SCHEDULE_BILL_LOG_STATUS = (
        (0, 'PENDING'),
        (1, 'COMPLETED'),
        (2, 'INPROGRESS'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_bill_id = models.BigIntegerField(null=False, blank=False)
    bill_cycle_id = models.BigIntegerField(null=False, blank=False)
    recurring_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    schedule_bill_log_status = models.IntegerField(choices=SCHEDULE_BILL_LOG_STATUS, default=0)
    date_and_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    @property
    def get_schedule_bill_name(self):
        schedule = get_schedule_bill_by_id(self.schedule_bill_id)
        return schedule

    @property
    def get_bill_cycle_name(self):
        bill_cycle = get_bill_cycle_by_id(self.bill_cycle_id)
        return bill_cycle

    @property
    def get_recurring_name(self):
        recurring = get_global_lookup_by_id(self.recurring_id)
        return recurring

    @property
    def get_utility_product_name(self):
        utility_product_type = get_utility_product_by_id(self.utility_product_id)
        return utility_product_type

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

# Create Schedule Table end


def get_schedule_bill_log_by_id(id):
    try:
        return ScheduleBillLog.objects.get(id=id, is_active=True)
    except:
        return False


def get_schedule_bill_log_by_id_string(id_string):
    try:
        return ScheduleBillLog.objects.get(id_string=id_string, is_active=True)
    except:
        return False
