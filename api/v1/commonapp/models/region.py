# Table Header
# Modules : Tenant, Utility | sub-modules : Tenant Master, Utility Master
# Table Type : Lookup (Global)
# Table Name : 2.12.4 Region
# Description : A global lookup table that stores regions.
# Frequency of data changes : Low
# Sample Table Data : "Americas", "Asia","Africa"
# Reference Table : 2.1 Utility Master
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from django.utils import timezone # importing package for datetime

# Create Region table start


class Region(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # @property
    # def get_currency(self):
    #     currency = get_region_by_id()(self.currency_id)
    #     return currency


def get_region_by_id(id):
    try:
        return Region.objects.get(id=id)
    except Exception as e:
        raise CustomAPIException("Region does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_region_by_id_string(id_string):
    try:
        return Region.objects.get(id_string=id_string)
    except:
        return False
# Create Region table end.
