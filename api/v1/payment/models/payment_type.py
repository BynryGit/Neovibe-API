# Table Header
# module: Consumer Care & Ops | sub-module - Consumer, Registration, Metering, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.20 Payment Type
# Description : It is a global lookup table that stores types of payments
# Frequency of data changes : Low
# Sample Table Data : "BillPayment" , "Service" , "Outstanding Recovery" , "Registration"
# Reference Table : 2.5.10 Payment Table.
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from django.db import models  # importing package for database

# Create Payment Type table start
class PaymentType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name + " " + str(self.id_string)

    def __unicode__(self):
        return self.name

def get_payment_type_by_id_string(id_string):
    try:
        return PaymentType.objects.get(id_string = id_string)
    except:
        return False

def get_payment_type_by_id(id):
    try:
        return PaymentType.objects.filter(id = id)
    except:
        return False
# Create Payment Type table end
