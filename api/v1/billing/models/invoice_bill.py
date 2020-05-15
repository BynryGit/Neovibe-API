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
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Invoice Bill Table Start.

class InvoiceBill(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    category = models.BigIntegerField(null=True, blank=True)
    subcategory = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    conversion_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    consumer_status = models.CharField(max_length=200, null=True, blank=True)
    cycle = models.BigIntegerField(null=True, blank=True)
    route = models.BigIntegerField(null=True, blank=True)
    utility_service_plan = models.BigIntegerField(null=True, blank=True)
    bill_count = models.BigIntegerField(null=True, blank=True)
    bill_month = models.CharField(max_length=200, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    billing_period_from = models.DateTimeField(null=True, blank=True, default=datetime.now())
    billing_period_to = models.DateTimeField(null=True, blank=True, default=datetime.now())
    meter_no = models.CharField(max_length=200, null=True, blank=True)
    meter_status = models.BigIntegerField(null=True, blank=True)
    meter_reading = models.BigIntegerField(null=True, blank=True)
    previous_reading = models.CharField(max_length=200, null=True, blank=True)
    current_reading = models.CharField(max_length=200, null=True, blank=True)
    previous_reading_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    current_reading_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    consumption = models.CharField(max_length=200, null=True, blank=True)
    basic_price = models.FloatField(null=True, blank=True)
    vat_percent = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    consumption_charges = models.FloatField(null=True, blank=True)
    net_amount = models.FloatField(null=True, blank=True)
    outstanding = models.FloatField(null=True, blank=True)
    payment = models.CharField(max_length=200, null=True, blank=True)
    current_charges = models.FloatField(null=True, blank=True)
    total_emi_paid = models.FloatField(null=True, blank=True)
    remaining_emi_amt = models.FloatField(null=True, blank=True)
    adjustments = models.CharField(max_length=200, null=True, blank=True)
    before_due_date_amount = models.FloatField(null=True, blank=True)
    after_due_date_amount = models.FloatField(null=True, blank=True)
    current_emi_amt = models.FloatField(null=True, blank=True)
    closing_month = models.CharField(max_length=200, null=True, blank=True)
    bill_status = models.BigIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_adjusted = models.BooleanField(default=False)
    is_spot_bill = models.BooleanField(default=False)
    is_sms_send = models.BooleanField(default=False)
    instruction = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)



    def __str__(self):
        return self.invoice_no

    def __unicode__(self):
        return self.invoice_no


def get_invoice_bills_by_consumer_no(consumer_no):
    return InvoiceBill.objects.filter(consumer_no = consumer_no)

# Create Invoice Bill table end.
