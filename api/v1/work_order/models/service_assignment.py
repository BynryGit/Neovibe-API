from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create Service Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.work_order.models.service_appointment_status import get_service_appointment_status_by_id
from master.models import get_user_by_id
from v1.work_order.models.service_appointments import get_service_appointment_by_id




# table header
# module: Work Order | sub-module -
# table type: Master
# table name: ServiceAssignment
# table description: It contains the list of ServiceAssignment
# #frequency of data changes: high
# sample table data:
# reference tables:
# Author : Priyanka Kachare
# Creation Date : 16/12/2020

class ServiceAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sa_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    assignment_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    assignment_time = models.TimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    completion_time = models.TimeField(null=True, blank=True)
    TAT = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    # def __str__(self):
    #     return self.id

    def __unicode__(self):
        return self.id

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_user(self):
        user_val = get_user_by_id(self.user_id)
        return {
            "name":user_val.first_name,
            "id_string":user_val.id_string,
            "email":user_val.email
        }

    @property
    def get_service_appointment(self):
        sa_val = get_service_appointment_by_id(self.sa_id)
        return sa_val
        # {
        #     "name":sa_val.sa_name,
        #     "number":sa_val.sa_number,
        #     "id_string":sa_val.id_string
        # }

    @property
    def get_status(self):
        status_val = get_service_appointment_status_by_id(self.status_id)
        return {
            "status":status_val.status,
            "id_string":status_val.id_string
        }

# Create service master table end

def get_service_assignment_by_tenant_id_string(id_string):
    return ServiceAssignment.objects.filter(tenant__id_string=id_string)


def get_service_assignment_by_utility_id_string(id_string):
    return ServiceAssignment.objects.filter(utility__id_string=id_string)


def get_service_assignment_by_id(id):
    try:
        return ServiceAssignment.objects.get(id=id)
    except:
        return False


def get_service_assignment_by_id_string(id_string):
    try:
        return ServiceAssignment.objects.get(id_string=id_string)
    except:
        return False

def get_service_assignment_by_appointment_id(id):
    try:
        return ServiceAssignment.objects.filter(sa_id=id,is_active=True)
    except:
        return False

