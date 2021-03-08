__author__ = "chinmay"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : SmartMeterConfiguration
# Description : It is SmartMeterConfiguration table. This table will save all the Configuration details of smart meter.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Chinmay Pathak
# Creation Date : 25/02/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from django.contrib.postgres.fields import JSONField
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_product import get_utility_product_by_id


# Create SmartMeterConfiguration Table Start

class SmartMeterConfiguration(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    smart_meter_api_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    api_url = models.CharField(max_length=200, blank=True, null=True)
    api_key = models.CharField(max_length=200, blank=True, null=True)
    request_parameter = JSONField()
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.smart_meter_api_name

    def __unicode__(self):
        return self.smart_meter_api_name

    @property
    def get_utility_product(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product


# Create SmartMeterConfiguration Table end


def get_smart_meter_configuration_by_id(id):
    try:
        return SmartMeterConfiguration.objects.get(id=id, is_active=True)
    except:
        return False


def get_smart_meter_configuration_by_id_string(id_string):
    try:
        return SmartMeterConfiguration.objects.get(id_string=id_string, is_active=True)
    except:
        return False

