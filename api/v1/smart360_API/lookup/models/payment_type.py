# Table Header : Payment Type
# Table Type : Lookup (Global)
# Table Name : 2.12.20 Payment Type
# Description : Payment Type and ID of Payment Type  to be used by Operator or Utility
# Frequency of data changes : Low
# Sample Table Data : BillPayment, Service, Outstanding Recovery
# Reference Table : 2.5.10 Payment Table.
# Auther : Jayshree
# Creation Date : 21-04-2020

import datetime
import uuid
from django.db import models

# Start the Code
class PaymentType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    payment_type = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_type

    def __unicode__(self):
        return self.payment_type
# End the Code