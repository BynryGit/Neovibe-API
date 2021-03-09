# Table Header
# Modules : MDM | sub-modules : Tenant Master, Utility Master
# Table Type : Lookup (Global)
# Table Name : 2.12.4 Region
# Description : A global lookup table that stores Meter Status.
# Frequency of data changes : Low
# Sample Table Data : "Normal", "RCNT","Faulty"
# Reference Table : 2.1 Utility Master
# Author : Chinmay Pathak
# Creation Date : 3-3-2021

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status


# Create Reader Status table start


class MeterStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    status_code = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # @property
    # def get_currency(self):
    #     currency = get_region_by_id()(self.currency_id)
    #     return currency


def get_meter_status_by_id(id):
    try:
        return MeterStatus.objects.get(id=id)
    except Exception as e:
        raise CustomAPIException("Meter Status does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_meter_status_by_id_string(id_string):
    try:
        return MeterStatus.objects.get(id_string=id_string)
    except:
        return False
# Create Reader Status table end.