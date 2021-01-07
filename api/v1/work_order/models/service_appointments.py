from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create Service Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.asset.models.asset_master import get_asset_by_id
from v1.work_order.models.work_order_master import get_work_order_master_by_id
from v1.work_order.models.service_appointment_status import get_service_appointment_status_by_id

class ServiceAppointment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    asset_id = models.BigIntegerField(blank=True, null=True)
    service_id = models.BigIntegerField(blank=True, null=True)
    sa_number = models.CharField(max_length=200, blank=True, null=True)
    sa_name = models.CharField(max_length=200, blank=True, null=True)
    sa_description = models.CharField(max_length=200, blank=True, null=True)
    sa_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    sa_time = models.TimeField(null=True, blank=True,default='20:00')
    sa_estimated_effort = models.BigIntegerField(null=True, blank=True)
    sa_rule = JSONField(default=[])
    sa_user_remark = models.CharField(max_length=200, blank=True, null=True)
    alternative_contact = models.CharField(max_length=200, blank=True, null=True)
    alternative_address = models.CharField(max_length=200, blank=True, null=True)
    actual_start_time = models.TimeField(null=True, blank=True,default='20:00')
    actual_end_time = models.TimeField(null=True, blank=True,default='20:00')
    actual_duration = models.BigIntegerField(blank=True, null=True)
    sa_area = models.CharField(max_length=200, blank=True, null=True)
    sa_sub_area = models.CharField(max_length=200, blank=True, null=True)
    sa_premises = models.CharField(max_length=200, blank=True, null=True)
    sa_GIS_id = models.BigIntegerField(blank=True, null=True)
    status_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.sa_number

    def __unicode__(self):
        return self.sa_number

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_consumer(self):
        consumer = get_consumer_by_id(self.consumer_id)
        return {
            "email_id":consumer.email_id,
            "id_string":consumer.id_string
        }

    @property
    def get_asset(self):
        asset = get_asset_by_id(self.asset_id)
        return {
            "name":asset.name,
            "id_string":asset.id_string
        }

    @property
    def get_service(self):
        work_order_template = get_work_order_master_by_id(self.service_id)
        return {
            "name":work_order_template.name,
            "id_string":work_order_template.id_string
        }
    
    @property
    def get_status(self):
        status_val = get_service_appointment_status_by_id(self.status_id)
        return {
            "status":status_val.status,
            "id_string":status_val.id_string
        }
        
# Create ServiceMaster table end


def get_service_appointment_by_tenant_id_string(id_string):
    return ServiceAppointment.objects.filter(tenant__id_string=id_string)


def get_service_appointment_by_utility_id_string(id_string):
    return ServiceAppointment.objects.filter(utility__id_string=id_string)


def get_service_appointment_by_id(id):
    try:
        return ServiceAppointment.objects.get(id=id)
    except:
        return False


def get_service_appointment_by_id_string(id_string):
    try:
        return ServiceAppointment.objects.get(id_string=id_string)
    except:
        return False
