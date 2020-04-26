# table header
# module: Purchase
# table type : Master
# table name : 2.7.5 Tender Quotation
# table description : The quotation table saves the quotation details according tender.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster


# Create Tender Quotation table start

class TenderQuotation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    tender = models.IntegerField(null=True, blank=True)
    vendor = models.IntegerField(null=True, blank=True)
    amount = models.CharField(max_length=200, blank=True, null=True)
    submission_date = models.DateField(null=True, blank=True, default=datetime.now())
    description = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id

# Create Tender Quotation table end
