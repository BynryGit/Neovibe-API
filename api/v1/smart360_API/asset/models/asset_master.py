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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Asset Master table start

class AsssetMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    asset_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    serial_no = models.IntegerField(null=True, blank=True)
    manufacturer = models.IntegerField(null=True, blank=True)
    make = models.IntegerField(null=True, blank=True)
    model = models.IntegerField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    sub_category_id = models.IntegerField(null=True, blank=True)
    asset_insurance_id = models.IntegerField(null=True, blank=True)
    insurance_no = models.CharField(max_length=200, blank=True, null=True)
    asset_amc_contract_id = models.IntegerField(null=True, blank=True)
    contract_no = models.CharField(max_length=200, blank=True, null=True)
    city_id = models.IntegerField(null=True, blank=True)
    area_id = models.IntegerField(null=True, blank=True)
    subarea_id = models.IntegerField(null=True, blank=True)
    Address = models.CharField(max_length=200, blank=True, null=True)
    lat = models.CharField(max_length=200, blank=True, null=True)
    lon = models.CharField(max_length=200, blank=True, null=True)
    manufacturing_date = models.DateField(null=True, blank=True, default=datetime.now())
    installation_date = models.DateField(null=True, blank=True, default=datetime.now())
    expiry_date = models.DateField(null=True, blank=True, default=datetime.now())
    asset_life = models.CharField(max_length=200, blank=True, null=True)
    asset_value = models.IntegerField(null=True, blank=True)
    deprication_method = models.IntegerField(null=True, blank=True)
    deprication_rate = models.IntegerField(null=True, blank=True)
    image = models.UrlField(null=False, blank=False)
    status_id = models.IntegerField(null=True, blank=True)
    flag = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.asset_name

# Create Asset Master table end.
