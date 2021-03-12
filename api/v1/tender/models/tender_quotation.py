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
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.tender.models.tender import get_tender_by_id
from v1.tender.models.tender_vendor import get_tender_vendor_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Tender Quotation table start

class TenderQuotation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tender_id = models.BigIntegerField(null=True, blank=True)
    vendor_id = models.BigIntegerField(null=True, blank=True)
    amount = models.CharField(max_length=200, blank=True, null=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description

    @property
    def get_tender(self):
        tender = get_tender_by_id(self.tender_id)
        return tender

    @property
    def get_vendor(self):
        vendor = get_tender_vendor_by_id(self.vendor_id)
        return vendor

# Create Tender Quotation table end


def get_tender_quotation_by_id(id):
    try:
        return TenderQuotation.objects.get(id=id)
    except:
        return False


def get_tender_quotation_by_id_string(id_string):
    try:
        return TenderQuotation.objects.get(id_string=id_string)
    except:
        return False
