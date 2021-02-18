__author__ = "aki"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : ConsumerMeter
# Description : It is consumer meter table. This table will save all the meter and consumer details.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Akshay Nibrad
# Creation Date : 18/02/2021


import uuid
from datetime import datetime
from django.db import models
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.meter_data_management.models.meter import get_meter_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class ConsumerMeter(models.Model):
    CONSUMER_METER_STATUS = (
        (0, 'CONNECTED'),
        (1, 'DISCONNECTED'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=False, blank=False)
    meter_id = models.BigIntegerField(null=False, blank=False)
    consumer_meter_status = models.IntegerField(choices=CONSUMER_METER_STATUS, default=0)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    @property
    def get_consumer_number(self):
        consumer = get_consumer_by_id(self.consumer_id)
        return consumer

    @property
    def get_meter_number(self):
        meter = get_meter_by_id(self.meter_id)
        return meter

    def __str__(self):
        return str(self.id_string)

    def __unicode__(self):
        return str(self.id_string)


def get_consumer_meter_by_id_string(id_string):
    try:
        return ConsumerMeter.objects.get(id_string=id_string, is_active=True)
    except:
        return False


def get_consumer_meter_by_id(id):
    try:
        return ConsumerMeter.objects.get(id=id, is_active=True)
    except:
        return False
