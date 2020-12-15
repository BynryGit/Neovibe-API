# table header
# module: S&M | sub-module - Campaign
# table type : lookup (Local)
# table name : 2.12.43 advertisement Subtypetype
# table description : A lookup table that stores various Subtypes of advertisement for campaign.
# frequency of data changes : Low
# sample table data : "tv_ads" , "canopy" , "fm_radio", "email" "linkedin" "google"
# reference tables : 2.3.6 advertisement master table
# author : Chinmay Pathak
# created on : 27/11/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.campaign.models.advertisement_type import get_advert_type_by_id

# Create advertisement Sub type table start.

class AdvertisementSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    adv_type_id = models.BigIntegerField(null=True, blank=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_advertisement_type(self):
        advertisement_type = get_advert_type_by_id(self.adv_type_id)
        return advertisement_type

def get_advert_subtype_by_id(id):
    return AdvertisementSubType.objects.filter(id = id)

def get_advert_subtype_by_id_string(id_string):
    try:
        return AdvertisementSubType.objects.get(id_string = id_string)
    except:
        return False
# Create advertisement Sub type table end.