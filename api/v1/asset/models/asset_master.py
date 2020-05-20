# table header
# module: Asset
# table type : Master
# table name : 2.6.2.1 Asset Master
# table description : It will store asset details related to service request and appointment.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Asset Master table start

class Assset(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    asset_no = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    serial_no = models.BigIntegerField(null=True, blank=True)
    manufacturer = models.BigIntegerField(null=True, blank=True)
    make = models.BigIntegerField(null=True, blank=True)
    model = models.BigIntegerField(null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    subarea_id = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    lat = models.CharField(max_length=200, blank=True, null=True)
    long = models.CharField(max_length=200, blank=True, null=True)
    manufacturing_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    installation_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    expiry_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    asset_life = models.CharField(max_length=200, blank=True, null=True)
    asset_value = models.BigIntegerField(null=True, blank=True)
    deprecation_method = models.BigIntegerField(null=True, blank=True)
    deprecation_rate = models.BigIntegerField(null=True, blank=True)
    image = models.UrlField(null=False, blank=False)
    status_id = models.BigIntegerField(null=True, blank=True)
    flag = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_status(self):
        status = get_cam_status_by_id(self.status_id)
        return status


def get_campaign_by_id_string(id_string):
    try:
        return Campaign.objects.get(id_string=id_string)
    except:
        return False


def get_campaign_by_id(id):
    try:
        return Campaign.objects.get(id=id)
    except:
        return False

# Create Asset Master table end.
