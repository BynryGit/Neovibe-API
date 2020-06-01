# table header
# module: O&M
# table type : Master
# table name : 2.6.4 Service Assignment
# table description :It will store the assign,deassign,reassign records of all service appointment.
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
from v1.commonapp.models.service_type import get_service_type_by_id
from v1.dispatcher.models.sop_status import get_sop_status_by_id
from v1.dispatcher.models.service_appointments import get_service_request_by_id
from v1.supplier.models.supplier import get_supplier_by_id
# Create Service Assignment table start

class ServiceAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_request_id = models.BigIntegerField(null=True, blank=True)
    service_type_id = models.BigIntegerField(null=True, blank=True)
    vendor_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    parent_record = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    assigned_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    completion_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    defined_duration = models.CharField(max_length=200, blank=True, null=True)
    actual_duration = models.CharField(max_length=200, blank=True, null=True)
    is_complete_on_time = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service_request_id)

    def __unicode__(self):
        return str(self.service_request_id)

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
    def get_sop_status(self):
        status_id = get_sop_status_by_id(self.status_id)
        return status_id

    @property
    def get_service_request(self):
        service_request_id = get_service_request_by_id(self.service_request_id)
        return service_request_id

    @property
    def get_vendor(self):
        vendor_id = get_supplier_by_id(self.vendor_id)
        return vendor_id

def get_service_assignment_by_id_string(id_string):
    try:
        return ServiceAssignment.objects.get(id_string=id_string)
    except:
        return False

def get_service_assignment_by_id(id):
    try:
        return ServiceAssignment.objects.get(id=id)
    except:
        return False


# Create Service Assignment table end.

