# Table Header : Payment Mode
# Table Type : Lookup (Global)
# Table Name : 2.12.19 Payment Mode
# Description : It Payment mode and ID of various Payment mode to be used by Operator or Utility
# Frequency of data changes : Low
# sample Table Data : Cash Payment, Cheque, self servie,dd, card,
# Reference Table : 2.3.1. Consumer Master, 2.7.2. Employee_bank_details, 2.7.8. Bank details.
# Auther : Jayshree
# Creation Date : 21-04-2020
import datetime
import uuid
from django.db import models

# Start the code
class PaymentMode(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    payment_mode = models.CharField(max_length=30, blank=False, null=False)
    bank_name = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_mode

    def __unicode__(self):
        return self.payment_mode
# End the Code