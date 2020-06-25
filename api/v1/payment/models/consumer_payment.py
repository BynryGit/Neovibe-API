import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
import fsm
from v1.payment.models.payment_channel import get_payment_channel_by_id
from v1.payment.models.payment_mode import get_payment_mode_by_id
from v1.payment.models.payment_source import get_payment_source_by_id
from v1.payment.models.payment_sub_type import get_payment_sub_type_by_id
from v1.payment.models.payment_type import get_payment_type_by_id
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster



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
# Create Consumer Payments Table Start.
class Payment(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        ('created', 'CREATED'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
    )

    state_machine = {
        'created': '__all__',
        'approved': ('approved',),
        'rejected': ('rejected',),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL, related_name='tenant')
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL, related_name='utility')
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=30, choices=CHOICES, default='created')
    payment_type_id = models.BigIntegerField(null=True, blank=True) # Registration, Bill Payment, services Charges
    payment_sub_type_id = models.BigIntegerField(null=True, blank=True) # Registration - Deposit, Rental, Processing Fees
    identification_id = models.BigIntegerField(null=True, blank=True) # registration No, Invoice #, service request no
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    transaction_amount = models.FloatField(blank=False, null=False)
    transaction_charges = models.FloatField(blank=False, null=False)
    transaction_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    payment_mode_id = models.BigIntegerField(null=True, blank=True)
    payment_channel_id = models.BigIntegerField(null=True, blank=True)
    payment_source_id = models.BigIntegerField(null=True, blank=True)
    receipt_no = models.CharField(max_length=200, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    account_no = models.CharField(max_length=200, null=True, blank=True)
    cheque_dd_no = models.CharField(max_length=200, null=True, blank=True)
    cheque_dd_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    ifsc_code = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    is_penalty = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.consumer_no) + '-' + str(self.payment_type) + '-' + str(self.payment_mode) + '-' + str(
            self.transaction_id)

    @property
    def get_payment_type(self):
        payment_type = get_payment_type_by_id(self.payment_type_id)
        return payment_type

    @property
    def get_payment_sub_type(self):
        payment_sub_type = get_payment_sub_type_by_id(self.payment_sub_type_id)
        return payment_sub_type

    @property
    def get_payment_mode(self):
        payment_mode = get_payment_mode_by_id(self.payment_mode_id)
        return payment_mode

    @property
    def get_payment_source(self):
        payment_source = get_payment_source_by_id(self.payment_source_id)
        return payment_source

    @property
    def get_payment_channel(self):
        payment_channel = get_payment_channel_by_id(self.payment_channel_id)
        return payment_channel

    def on_change_state(self, previous_state, next_state, **kwargs):
        self.save()


def get_payment_by_id_string(id_string):
    try:
        return Payment.objects.get(id_string = id_string)
    except:
        return False


def get_payments_by_consumer_no(consumer_no):
    try:
        return Payment.objects.filter(consumer_no = consumer_no)
    except:
        return False

# Create Consumer Payment table end.
