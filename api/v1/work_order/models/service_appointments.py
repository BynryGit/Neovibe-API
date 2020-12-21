from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create Service Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class ServiceAppointment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    Asset_id = models.BigIntegerField(blank=True, null=True)
    service_id = models.BigIntegerField(blank=True, null=True)
    sa_number = models.CharField(max_length=200, blank=True, null=True)
    sa_name = models.CharField(max_length=200, blank=False, null=False)
    sa_description = models.CharField(max_length=200, blank=True, null=True)
    sa_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    sa_time = models.TimeField()
    sa_estimated_effort = models.BigIntegerField(null=True, blank=True)
    json_obj = JSONField()
    sa_user_remark = models.CharField(max_length=200, blank=True, null=True)
    alternative_contact = models.CharField(max_length=200, blank=True, null=True)
    alternative_address = models.CharField(max_length=200, blank=True, null=True)
    actual_start_time = models.TimeField()
    actual_end_time = models.TimeField()
    actual_duration = models.BigIntegerField(blank=True, null=True)
    sa_area = models.CharField(max_length=200, blank=True, null=True)
    sa_sub_area = models.CharField(max_length=200, blank=True, null=True)
    sa_premises = models.CharField(max_length=200, blank=True, null=True)
    sa_rule = JSONField()
    sa_GIS_id = models.BigIntegerField(blank=False, null=False)
    status = models.BigIntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.sa_name

    def __unicode__(self):
        return self.sa_name
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
