# Table Header
# Module: Consumer Care | Sub-Module : Meter Reading, Billing
# Table Type : Master (Global)
# Table Name : 2.4.7. Consumer - Meter
# Description : It will save all active and inactive consumers and associated meters for given tenant.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database


# Create Consumer Meter Table Start.

class ConsumerMeter(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer = models.BigIntegerField(null=True, blank=True)
    meter_id = models.BigIntegerField(null=True, blank=True)
    assign_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    initial_reading = models.BigIntegerField(null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.meter_id) + '-' + str(self.consumer_id) + '-' + str(self.assign_date) + '-' + str(
            self.initial_reading) + '-' + str(self.status)
# Create Consumer meter table end.

def get_consumer_meter_by_id(id):
    try:
        return ConsumerMeter.objects.get(id=id)
    except:
        return False


def get_consumer_meter_by_id_string(id_string):
    try:
        return ConsumerMeter.objects.get(id_string=id_string)
    except:
        return False
