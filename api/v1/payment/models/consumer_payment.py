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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Consumer Payments Table Start.

class ConsumerPayments(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    payment_type = models.IntegerField(null=True, blank=True) # Registration, Bill Payment, services Charges
    payment_subtype = models.IntegerField(null=True, blank=True) # Registration - Deposit, Rental, Processing Fees
    identification = models.IntegerField(null=True, blank=True) # registration No, Invoice #, service request no
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    transaction_amount = models.FloatField(blank=False, null=False)
    transaction_charges = models.FloatField(blank=False, null=False)
    transaction_date = models.DateField(null=True, blank=True, default=datetime.now())
    payment_mode = models.IntegerField(null=True, blank=True)
    payment_channel = models.IntegerField(null=True, blank=True)
    payment_provider = models.IntegerField(null=True, blank=True)
    receipt_no = models.CharField(max_length=200, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    account_no = models.CharField(max_length=200, null=True, blank=True)
    cheque_dd_no = models.CharField(max_length=200, null=True, blank=True)
    cheque_dd_date = models.DateField(null=True, blank=True, default=datetime.now())
    ifsc_code = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.consumer_no) + '-' + str(self.payment_type) + '-' + str(self.payment_mode) + '-' + str(
            self.transaction_id)

# Create Consumer Payment table end.
