# table header
# module: Sourcing
# table type : Master
# table name : Document
# table description : The Document table saves the Document details of all the modules that need documents against them.
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

from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster

# Create Document Demand Table start


class Documents(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    module = models.IntegerField(null=True, blank=True)
    sub_module = models.IntegerField(null=True, blank=True)
    servicetype = models.IntegerField(null=True, blank=True)
    identification = models.IntegerField(null=True, blank=True)
    document_type = models.IntegerField(null=True, blank=True)
    document_subtype = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    doc_link = models.UrlField(null=False, blank=False)
    status_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.identification

    def __unicode__(self):
        return self.identification

# Create Document table end.

