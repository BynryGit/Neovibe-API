# table header
# module: O&M
# table type : Master
# table name : 2.6.1 Service Request
# table description : It is service appointment table. It will store the appointment of each service type.
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
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.asset.models.asset_master import get_asset_by_id
from v1.commonapp.models.service_type import get_service_type_by_id
from v1.dispatcher.models.sop_status import get_sop_status_by_id
# Create Service Request table start

class ServiceRequest(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_type_id = models.BigIntegerField(null=True, blank=True)
    service_no = models.CharField(max_length=500, blank=True, null=True)
    service_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    consumer_address = models.CharField(max_length=200, blank=True, null=True)
    asset_id = models.BigIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    parent_record = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    effort_duration = models.CharField(max_length=200, blank=True, null=True)
    flag = models.BooleanField(default=False)
    priority = models.BigIntegerField(null=True, blank=True)
    skill = models.BigIntegerField(null=True, blank=True)#user skill
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.service_no) + '-' + str(self.service_name)

    def __unicode__(self):
        return str(self.service_no) + '-' + str(self.service_name)

    @property
    def get_service_type(self):
        service_type_id = get_service_type_by_id(self.service_type_id)
        return service_type_id

    @property
    def get_city(self):
        city_id = get_city_by_id(self.city_id)
        return city_id

    @property
    def get_area(self):
        area_id = get_area_by_id(self.area_id)
        return area_id

    @property
    def get_sub_area(self):
        sub_area_id = get_sub_area_by_id(self.sub_area_id)
        return sub_area_id

    @property
    def get_consumer(self):
        consumer_id = get_consumer_by_id(self.consumer_id)
        return consumer_id

    @property
    def get_asset(self):
        asset_id = get_asset_by_id(self.asset_id)
        return asset_id

    @property
    def get_sop_status(self):
        status_id = get_sop_status_by_id(self.status_id)
        return status_id

def get_service_request_by_id_string(id_string):
    try:
        return ServiceRequest.objects.get(id_string=id_string)
    except:
        return False

def get_service_request_by_id(id):
    try:
        return ServiceRequest.objects.get(id=id)
    except:
        return False

# Create Service Request table end.


