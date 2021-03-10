# table header
# module: Sourcing
# table type : Master
# table name : Tender Terms & Conditions
# table description : The Terms table saves the terms and condition details of tender
# frequency of data changes : High
# sample table data : "Condition 1", "Condition 2"
# reference tables : None
# author : Akshay
# created on : 09/06/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.tender.models.tender import get_tender_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Terms And Condition Table start

class TenderTermsAndCondition(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    tender_id = models.BigIntegerField(null=True, blank=True)
    terms_name = models.CharField(max_length=200, blank=True, null=True)
    terms = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.terms_name

    def __unicode__(self):
        return self.terms_name

    @property
    def get_tender(self):
        tender = get_tender_by_id(self.tender_id)
        return tender

# Create Terms and Conditions table end.


def get_tender_term_and_condition_by_id(id):
    try:
        return TenderTermsAndCondition.objects.get(id=id)
    except:
        return False


def get_tender_term_and_condition_by_id_string(id_string):
    try:
        return TenderTermsAndCondition.objects.get(id_string=id_string)
    except:
        return False
