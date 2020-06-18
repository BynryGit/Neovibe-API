# table header
# module: Purchase
# table type : Master
# table name : 2.7.4 Tender - Vendor
# table description : This table store all vendor details according to tender.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from master.models import get_user_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.tender.models.tender import get_tender_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Tender - Vendor table start

class TenderVendor(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tender_id = models.BigIntegerField(null=True, blank=True)
    vendor_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)

    @property
    def get_tender(self):
        tender = get_tender_by_id(self.tender_id)
        return tender

    @property
    def get_vendor(self):
        vendor = get_user_by_id(self.vendor_id)
        return vendor

# Create Tender  - Vendor table end.


def get_tender_vendor_by_id(id):
    try:
        return TenderVendor.objects.get(id=id)
    except:
        return False


def get_tender_vendor_by_id_string(id_string):
    try:
        return TenderVendor.objects.get(id_string=id_string)
    except:
        return False