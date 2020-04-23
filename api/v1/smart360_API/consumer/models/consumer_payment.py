# Table Header
# Module: Consumer Care
# Table Type : Master (Global)
# Table Name : 2.3.13. Consumer - Payments
# Description : It will store the all consumer payment details
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Consumer Payments Table Start.

class ConsumerPayments(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(null=True, blank=True)
    payment_type = models.IntegerField(null=True, blank=True)
    identification_id = models.IntegerField(null=True, blank=True)
    payment_mode = models.IntegerField(null=True, blank=True)
    payment_channel = models.IntegerField(null=True, blank=True)
    payment_provider = models.IntegerField(null=True, blank=True)
    transaction_id = models.CharField(null=True, blank=True)
    transaction_amount = models.FloatField(blank=False, null=False)
    transaction_charges = models.FloatField(blank=False, null=False)
    transaction_date = models.DateField(null=True, blank=True, default=datetime.now())
    receipt_no = models.CharField(null=True, blank=True)
    bank_name = models.IntegerField(null=True, blank=True)
    account_no = models.CharField(null=True, blank=True)
    cheque_dd_no = models.CharField(null=True, blank=True)
    cheque_dd_date = models.DateField(null=True, blank=True, default=datetime.now())
    ifsc_code = models.CharField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(str(self.consumer_no) + '-' + str(self.payment_type) + '-' + str(self.payment_mode) + '-' + str(self.transaction_id))


# Create Consumer Payment table end.


