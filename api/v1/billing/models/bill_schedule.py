# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : schedule bill
# table description : A lookup table for  schedule of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : schedule bill Table
# author : Priyanka 
# created on : 01/03/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField
from v1.utility.models.utility_product import get_utility_product_by_id

# Create Bill Frequency table start.

class ScheduleBill(models.Model):
    SCHEDULE_STATUS = (
        (0, 'PENDING'),
        (1, 'COMPLETED'),
        (2, 'INPROGRESS'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    frequency_id = models.BigIntegerField(null=True, blank=True)
    repeat_every_id = models.BigIntegerField(null=True, blank=True)
    recurring_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    occurs_on = JSONField(default=[])
    cron_expression = models.CharField(max_length=500, blank=True, null=True)
    schedule_status = models.IntegerField(choices=SCHEDULE_STATUS, default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.bill_cycle_id)

    def __unicode__(self):
        return self.bill_cycle_id

    @property
    def get_bill_cycle_name(self):
        bill_cycle = get_bill_cycle_by_id(self.bill_cycle_id)
        return bill_cycle

    @property
    def get_frequency_name(self):
        frequency = get_global_lookup_by_id(self.frequency_id)
        return frequency

    @property
    def get_repeat_every_name(self):
        repeat_every = get_global_lookup_by_id(self.repeat_every_id)
        return repeat_every

    @property
    def get_recurring_name(self):
        recurring = get_global_lookup_by_id(self.recurring_id)
        return recurring

    @property
    def get_utility_product_name(self):
        utility_product_type = get_utility_product_by_id(self.utility_product_id)
        return utility_product_type


# Create Bill Frequency table end.

def get_schedule_bill_by_tenant_id_string(tenant_id_string):
    return ScheduleBill.objects.filter(tenant__id_string=tenant_id_string)

def get_schedule_bill_by_id_string(id_string):
    try:
        return ScheduleBill.objects.get(id_string = id_string)
    except:
        return False

def get_schedule_bill_by_id(id):
    try:
        return ScheduleBill.objects.get(id = id)
    except:
        return False