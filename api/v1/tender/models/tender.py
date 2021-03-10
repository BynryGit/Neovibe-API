# table header
# module: Purchase
# table type : Master
# table name : 2.7.3 Tender
# table description : This table will store all tender details.
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
from v1.tender.models.tender_status import get_tender_status_by_id
from v1.tender.models.tender_type import get_tender_type_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Tender Master table start

class Tender(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tender_no = models.CharField(max_length=200, blank=True, null=True)
    tender_name = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    type_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    pre_bidding_date = models.DateTimeField(null=True, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    eic_name = models.CharField(max_length=200, blank=True, null=True)
    eic_contact_no = models.CharField(max_length=200, blank=True, null=True)
    amount = models.BigIntegerField(null=True, blank=True)
    department = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    asset = models.BigIntegerField(null=True, blank=True)
    country_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tender_name

    def __unicode__(self):
        return self.tender_name

    @property
    def get_tender_status(self):
        tender = get_tender_status_by_id(self.status_id)
        return tender

    @property
    def get_tender_type(self):
        tender = get_tender_type_by_id(self.type_id)
        return tender

# Create Tender Master table end.


def get_tender_by_id(id):
    try:
        return Tender.objects.get(id=id)
    except:
        return False


def get_tender_by_id_string(id_string):
    try:
        return Tender.objects.get(id_string=id_string)
    except:
        return False
