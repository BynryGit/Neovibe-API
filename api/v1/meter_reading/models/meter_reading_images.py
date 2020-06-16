# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading , Validation
# Table Type : Master (Global)
# Table Name : 2.3.8.5 Meter Reading Images
# Description : It is meter reading images table for saving images readingwise.
# Frequency of data changes : High
# Sample table : "Meter Images"
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime
from api.constants import get_file_name, METER_PICTURE
from master.models import get_user_by_id
from v1.meter_reading.models.meter_image_type import get_meter_image_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Meter Reading Table Start

def get_file_path(instance, filename):
    return get_file_name(METER_PICTURE, filename)


class MeterImage(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    meter_reading_id = models.BigIntegerField(null=True, blank=True)
    type_id = models.BigIntegerField(null=True, blank=True)
    meter_image = models.FileField(upload_to=get_file_path, null=False, blank=False)
    # image_url = models.UrlField(null=False, blank=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

    @property
    def get_meter_reader(self):
        route = get_user_by_id(self.meter_reading_id)
        return route

    @property
    def get_meter_image_type(self):
        meter_reader = get_meter_image_type_by_id(self.type_id)
        return meter_reader

# Create Meter Reading Images Table End


def get_meter_image_by_id(id):
    try:
        return MeterImage.objects.get(id=id)
    except:
        return False


def get_meter_image_id_string(id_string):
    try:
        return MeterImage.objects.get(id_string=id_string)
    except:
        return False
