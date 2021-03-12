import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from api.messages import *
from django.utils import timezone # importing package for datetime


# Create Utility Document Type table start


class UtilityDocumentType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    document_type_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    document_size = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # @property
    # def get_currency(self):
    #     currency = get_region_by_id()(self.currency_id)
    #     return currency


def get_utility_document_type_by_id(id):
    try:
        document_type = UtilityDocumentType.objects.get(id=id)
        return document_type
    except Exception as e:
        return False


def get_utility_document_type_by_id_string(id_string):
    try:
        return UtilityDocumentType.objects.get(id_string=id_string)
    except:
        return False
# Create Utility Document Type table end.
