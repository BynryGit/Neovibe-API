# Table Header
# Module: Consumer Care | Sub-Module : Billing
# Table Type : Master (Global)
# Table Name : 2.3.13. Consumer - Payments
# Description : It will store the all consumer payment details
# Frequency of data changes : High
# Sample table : "Payment Details"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Consumer Payments Table Start.

class ConsumerPayments(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    payment_type = models.BigIntegerField(null=True, blank=True) # Registration, Bill Payment, services Charges
    payment_subtype = models.BigIntegerField(null=True, blank=True) # Registration - Deposit, Rental, Processing Fees
    identification = models.BigIntegerField(null=True, blank=True) # registration No, Invoice #, service request no
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    transaction_amount = models.FloatField(blank=False, null=False)
    transaction_charges = models.FloatField(blank=False, null=False)
    transaction_date = models.DateField(null=True, blank=True, default=datetime.now())
    payment_mode = models.BigIntegerField(null=True, blank=True)
    payment_channel = models.BigIntegerField(null=True, blank=True)
    payment_provider = models.BigIntegerField(null=True, blank=True)
    receipt_no = models.CharField(max_length=200, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    account_no = models.CharField(max_length=200, null=True, blank=True)
    cheque_dd_no = models.CharField(max_length=200, null=True, blank=True)
    cheque_dd_date = models.DateField(null=True, blank=True, default=datetime.now())
    ifsc_code = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.consumer_no) + '-' + str(self.payment_type) + '-' + str(self.payment_mode) + '-' + str(
            self.transaction_id)

# Create Consumer Payment table end.
