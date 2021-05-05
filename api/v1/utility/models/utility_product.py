import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from django.utils import timezone # importing package for datetime


# Create UtilityProduct table start


class UtilityProduct(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    product_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + " - " + str(self.id_string)

    def __unicode__(self):
        return self.name


def get_utility_product_by_id(id):
    try:
        return UtilityProduct.objects.get(id=id)
    except:
        return False


def get_utility_product_by_id_string(id_string):
    try:
        return UtilityProduct.objects.get(id_string=id_string)
    except:
        return False


def get_utility_product_by_name(name):
    try:
        return UtilityProduct.objects.get(name=name)
    except:
        return False
# Create UtilityProduct table end.
