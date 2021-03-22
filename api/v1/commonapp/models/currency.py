# Table Header
# module: Consumer Care & Ops | sub-module - Consumer, Registration, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.11 Currency
# Description : It is a global lookup table that stores the currencies with respect to the countries
# Frequency of data changes : Low
# Sample Table Data : "Rupee", "Pound", "Dollar"
# Reference Table : 2.2.2 Service Plans, 2.3.13. Consumer - Payments, 2.5.2 Contracts Table
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020


import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime

from django.db import models  # importing package for database

# Create Currency table start
from rest_framework import status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone  # importing package for datetime


class Currency(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    key = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def get_currency_by_id(id):
    try:
        return Currency.objects.get(id=id)
    except Exception as e:
        raise CustomAPIException("Currency not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_currency_by_id_string(id_string):
    try:
        return Currency.objects.get(id_string=id_string)
    except Exception as e:
        raise CustomAPIException("Currency not exists.", status_code=status.HTTP_404_NOT_FOUND)
