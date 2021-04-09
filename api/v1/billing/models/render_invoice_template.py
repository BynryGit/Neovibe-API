# table header
# module: billing | sub-module - billing
# table type : Master
# table name : Render Invoice Template
# table description : A lookup table for  Render Invoice Template of given Invoice.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Render Invoice Template Table
# author : Priyanka 
# created on : 06/04/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create Render Invoice Template table start.

class RenderInvoiceTemplate(models.Model):
    RENDERING_TYPE = (
        (0, 'PDF'),
        (1, 'HTML'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    invoice_section_master_id = models.BigIntegerField(null=True, blank=True)
    rendering_template_key = models.CharField(max_length=200, null=True, blank=True)
    rendering_type = models.IntegerField(choices=RENDERING_TYPE, default=0)
    rendering_template = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.rendering_template_key

    def __unicode__(self):
        return self.rendering_template_key

# Create Render Invoice Template table end.


def get_rendering_invoice_template_by_id_string(id_string):
    try:
        return RenderInvoiceTemplate.objects.get(id_string = id_string)
    except:
        return False

def get_rendering_invoice_template_by_id(id):
    try:
        return RenderInvoiceTemplate.objects.get(id = id)
    except:
        return False