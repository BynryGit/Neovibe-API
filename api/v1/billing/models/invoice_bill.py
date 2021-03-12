# Table Header
# Module: Consumer Care & Ops | Sub-Module : Billing
# Table Type : Master (Global)
# Table Name : 2.4.9 Invoice/Bill
# Description : It is billing details table. it contains all record related to billing for each consumer month wise.
# Frequency of data changes : High
# Sample table : "Bill 1", "Bill 2"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from django.utils import timezone # importing package for datetime
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Invoice Bill Table Start.

class InvoiceBill(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    conversion_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    consumer_status = models.CharField(max_length=200, null=True, blank=True)
    cycle_id = models.BigIntegerField(null=True, blank=True)
    route_id = models.BigIntegerField(null=True, blank=True)
    utility_service_plan_id = models.BigIntegerField(null=True, blank=True)
    bill_count = models.BigIntegerField(null=True, blank=True)
    bill_month = models.CharField(max_length=200, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    meter_status = models.BigIntegerField(null=True, blank=True)
    meter_reading = models.BigIntegerField(null=True, blank=True)
    previous_reading = models.FloatField(null=True, blank=True)
    current_reading = models.FloatField(null=True, blank=True)
    previous_reading_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    current_reading_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    consumption = models.FloatField(null=True, blank=True)
    basic_price = models.FloatField(null=True, blank=True)
    vat_percent = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    consumption_charges = models.FloatField(null=True, blank=True)
    net_amount = models.FloatField(null=True, blank=True)
    outstanding = models.FloatField(null=True, blank=True)
    payment = models.FloatField(null=True, blank=True)
    current_charges = models.FloatField(null=True, blank=True)
    total_emi_paid = models.FloatField(null=True, blank=True)
    remaining_emi_amt = models.FloatField(null=True, blank=True)
    adjustments = models.CharField(max_length=200, null=True, blank=True)
    before_due_date_amount = models.FloatField(null=True, blank=True)
    after_due_date_amount = models.FloatField(null=True, blank=True)
    current_emi_amt = models.FloatField(null=True, blank=True)
    closing_month = models.CharField(max_length=200, null=True, blank=True)
    bill_status_id = models.BigIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_adjusted = models.BooleanField(default=False)
    is_spot_bill = models.BooleanField(default=False)
    is_sms_send = models.BooleanField(default=False)
    instruction_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=False)



    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

    @property
    def get_category(self):
        try:
            category = get_consumer_category_by_id(self.category_id)
            return  category
        except:
            return False

    @property
    def get_sub_category(self):
        try:
            sub_category = get_consumer_sub_category_by_id(self.sub_category_id)
            return sub_category
        except:
            return False


def get_invoice_bills_by_consumer_no(consumer_no):
    return InvoiceBill.objects.filter(consumer_no = consumer_no)


def get_invoice_bill_by_id_string(id_string):
    try:
        return InvoiceBill.objects.get(id_string=id_string)
    except:
        return False


def get_invoice_bill_by_id(id):
    try:
        return InvoiceBill.objects.get(id=id)
    except:
        return False


def get_consumer_invoice_bill_by_month(consumer, month):
    try:
        return InvoiceBill.objects.get(consumer_no = consumer, bill_month = month)
    except:
        return False


def get_previous_consumer_bill(consumer):
    try:
        return InvoiceBill.objects.filter(consumer_no = consumer)[InvoiceBill.objects.filter(consumer_no = consumer).count()-2]
    except:
        return False
