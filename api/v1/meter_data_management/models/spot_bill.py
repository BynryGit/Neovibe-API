__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : Spot Bill
# Description : It is Spot Bill table. This table will save all the Bill details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 30/03/2021

from django.utils import timezone # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Temp Spot Bill Table Start

class SpotBill(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_detail_id = models.BigIntegerField(null=True, blank=True)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)
    consumption = models.CharField(max_length=200, null=True, blank=True)
    consumption_charges = models.CharField(max_length=200, null=True, blank=True)
    basic_price = models.CharField(max_length=200, null=True, blank=True)
    vat_percentage = models.CharField(max_length=200, null=True, blank=True)
    total_price = models.CharField(max_length=200, null=True, blank=True)
    net_amount = models.CharField(max_length=200, null=True, blank=True)
    previous_balance = models.CharField(max_length=200, null=True, blank=True)
    current_charges = models.CharField(max_length=200, null=True, blank=True)
    emi_security_deposit = models.CharField(max_length=200, null=True, blank=True)
    current_emi_amount = models.CharField(max_length=200, null=True, blank=True)
    remaining_emi_amount = models.CharField(max_length=200, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    bill_period_from = models.DateTimeField(null=True, blank=True)
    bill_period_to = models.DateTimeField(null=True, blank=True)
    before_due_date = models.DateTimeField(null=True, blank=True)
    after_due_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_adjusted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

# Create Temp Spot Bill Table end


def get_spot_bill_by_id(id):
    try:
        return SpotBill.objects.get(id=id)
    except:
        return False


def get_spot_bill_by_id_string(id_string):
    try:
        return SpotBill.objects.get(id_string=id_string)
    except:
        return False
