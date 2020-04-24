# table header
# module: Sourcing
# table type : Master
# table name : 2.5.11 Terms & Conditions
# table description : The Terms table saves the terms and condition details of Supplier or Contract
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Terms And Condition Table start

class TermsAndCondition(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module_id = models.IntegerField(null=True, blank=True)
    sub_module_id = models.IntegerField(null=True, blank=True)
    terms_name = models.CharField(max_length=200, blank=True, null=True)
    terms = models.CharField(max_length=200, blank=True, null=True)
    status_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Terms and Conditions table end.
