# table header
# module: S&M,Consumer care and ops | sub-module - Registration
# table type : Master
# table name : 2.4.2 Registration Master
# table description : A master table to store new registration details.
# frequency of data changes : High
# sample table data : "Registration 1" , "Registration 2" , "Registration 3"
# reference tables : None
# author : Rohan Wagh
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

from datetime import datetime # importing package for datetime

from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.registration.models.registration_status import get_registration_status_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid
from django.db import models
# Remove all fields as compulsory
# Create Consumer Registration table start.
class Registration(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    registration_no = models.CharField(max_length=200, blank=True, null=True)
    registration_type_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    phone_mobile = models.BigIntegerField(null=True, blank=True)
    phone_landline = models.BigIntegerField(null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200,null=True, blank=True)
    country_id = models.BigIntegerField(null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    scheme_id = models.BigIntegerField(null=True, blank=True)
    payment_id = models.BigIntegerField(null=True, blank=True)
    ownership_id = models.BigIntegerField(null=True, blank=True)
    consumer_category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    connectivity = models.BooleanField(default=False)
    registration_channel_id = models.BigIntegerField(null=True, blank=True)
    source_id = models.BigIntegerField(null=True, blank=True)
    registration_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.first_name

    def __unicode__(self):
        return self.first_name

    @property
    def get_status(self):
        status = get_registration_status_by_id(self.status_id)
        return status

    @property
    def get_area(self):
        area = get_area_by_id(self.area_id)
        return area



def get_registration_by_id_string(id_string):
    try:
        return Registration.objects.get(id_string = id_string)
    except:
        return  False
# Create Consumer Registration table end.