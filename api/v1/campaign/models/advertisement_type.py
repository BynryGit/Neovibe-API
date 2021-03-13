# table header
# module: S&M | sub-module - Campaign
# table type : lookup (Local)
# table name : 2.12.43 advertisement type
# table description : A lookup table that stores various types of advertisement for campaign.
# frequency of data changes : Low
# sample table data : "tv_ads" , "canopy" , "fm_radio", "email" "linkedin" "google"
# reference tables : 2.3.6 advertisement master table
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create advertisement type table start.

class AdvertisementType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

def get_advert_type_by_id(id):
    return AdvertisementType.objects.filter(id = id)

def get_advert_type_by_id_string(id_string):
    try:
        return AdvertisementType.objects.get(id_string = id_string)
    except:
        return False
# Create advertisement type table end.
