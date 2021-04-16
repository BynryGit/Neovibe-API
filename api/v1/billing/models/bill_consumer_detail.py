__author__ = "priyanka"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : billing, Bill Distribution
# Table Type : Master
# Table Name : Bill Consumer Deatils
# Description : It is consumer table. This table will save all the consumer details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Priyanka
# Creation Date : 08/03/2021

from django.utils import timezone # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.billing.models.bill_schedule_log import get_schedule_bill_log_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id
# Create Temp Bill Consumer Master Table Start

class BillConsumerDetail(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    meter_id = models.BigIntegerField(null=True, blank=True)
    bill_schedule_log_id = models.BigIntegerField(null=True, blank=True)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_bill_cycle_name(self):
        bill_cycle = get_bill_cycle_by_id(self.bill_cycle_id)
        return bill_cycle

    def get_schedule_log(self):
        bill_schedule_log = get_schedule_bill_log_by_id(self.bill_schedule_log_id)
        return bill_schedule_log

    def get_consumer(self):
        consumer = get_consumer_by_id(self.consumer_id)
        return consumer

# Create Temp Bill Consumer Master Table end


def get_bill_consumer_detail_by_id(id):
    try:
        return BillConsumerDetail.objects.get(id=id)
    except:
        return False


def get_bill_consumer_detail_by_id_string(id_string):
    try:
        return BillConsumerDetail.objects.get(id_string=id_string)
    except:
        return False


def get_bill_consumer_detail_by_schedule_log_id(id):
    try:
        return BillConsumerDetail.objects.filter(bill_schedule_log_id=id, is_active=True)
    except:
        return False