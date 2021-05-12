from datetime import datetime # importing package for datetime
import uuid
from v1.commonapp.views.custom_exception import CustomAPIException  # importing package for GUID
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField
import fsm

# Create Service Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.asset.models.asset_master import get_asset_by_id
from v1.work_order.models.work_order_master import get_work_order_master_by_id
from v1.work_order.models.service_appointment_status import get_service_appointment_status_by_id
from rest_framework import status
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id
from django.utils import timezone # importing package for datetime
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id

# *********** SERVICE APPOINTMENT CONSTANTS **************
SERVICE_APPOINTMENT_DICT = {
    "CREATED": 0,
    "NOT ASSIGNED": 1,
    "ASSIGNED": 2,
    "IN PROGRESS": 3,
    "FAILED": 4,
    "ACCEPTED": 5,
    "REJECTED": 6,
    "COMPLETED": 7,
    "HOLD": 8,
    "CLOSED": 9,
    "ARCHIVED": 10,
    "REQUESTED": 11,
}


# table header
# module: Work Order
# table type : Master
# table name : Service Appointment
# table description : A master table to store new ServiceAppointment
# frequency of data changes : High
# sample table data : 
# reference tables : None
# author : Priyanka
# created on : 13/01/2021

# Create Service Appointment table start.
class ServiceAppointment(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'NOT ASSIGNED'),
        (2, 'ASSIGNED'),
        (3, 'IN PROGRESS'),
        (4, 'FAILED'),
        (5, 'ACCEPTED'),
        (6, 'REJECTED'),
        (7, 'COMPLETED'),
        (8, 'HOLD'),
        (9, 'CLOSED'),
        (10, 'ARCHIVED'),
        (11, 'REQUESTED')
    )

    state_machine = {
        SERVICE_APPOINTMENT_DICT['CREATED']: (SERVICE_APPOINTMENT_DICT['NOT ASSIGNED'],SERVICE_APPOINTMENT_DICT['REQUESTED'],),
        SERVICE_APPOINTMENT_DICT['REQUESTED']: (SERVICE_APPOINTMENT_DICT['CREATED'],SERVICE_APPOINTMENT_DICT['REJECTED'],SERVICE_APPOINTMENT_DICT['NOT ASSIGNED'],SERVICE_APPOINTMENT_DICT['HOLD'],),
        SERVICE_APPOINTMENT_DICT['NOT ASSIGNED']: (SERVICE_APPOINTMENT_DICT['ASSIGNED'],SERVICE_APPOINTMENT_DICT['FAILED'],SERVICE_APPOINTMENT_DICT['IN PROGRESS'],),
        SERVICE_APPOINTMENT_DICT['ASSIGNED']: (SERVICE_APPOINTMENT_DICT['ACCEPTED'],SERVICE_APPOINTMENT_DICT['REJECTED'],SERVICE_APPOINTMENT_DICT['NOT ASSIGNED'],),
        SERVICE_APPOINTMENT_DICT['REJECTED']: (SERVICE_APPOINTMENT_DICT['ASSIGNED'],),
        SERVICE_APPOINTMENT_DICT['ACCEPTED']: (SERVICE_APPOINTMENT_DICT['COMPLETED'],),
        SERVICE_APPOINTMENT_DICT['COMPLETED']: (SERVICE_APPOINTMENT_DICT['HOLD'], SERVICE_APPOINTMENT_DICT['CLOSED'],),
        SERVICE_APPOINTMENT_DICT['HOLD']: (SERVICE_APPOINTMENT_DICT['ASSIGNED'], SERVICE_APPOINTMENT_DICT['CLOSED'],SERVICE_APPOINTMENT_DICT['REJECTED'],SERVICE_APPOINTMENT_DICT['NOT ASSIGNED'],),
        SERVICE_APPOINTMENT_DICT['CLOSED']: (SERVICE_APPOINTMENT_DICT['ARCHIVED'],),
    }
    
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_service_contract_detail_id = models.BigIntegerField(null=True, blank=True)
    asset_id = models.BigIntegerField(blank=True, null=True)
    work_order_master_id = models.BigIntegerField(blank=True, null=True)
    state = models.BigIntegerField(choices=CHOICES, default=1)
    sa_number = models.CharField(max_length=200, blank=True, null=True)
    sa_name = models.CharField(max_length=200, blank=True, null=True)
    sa_description = models.CharField(max_length=200, blank=True, null=True)
    sa_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    sa_estimated_effort = models.BigIntegerField(null=True, blank=True)
    sa_rule = JSONField(null=True, blank=True)
    sa_user_remark = models.CharField(max_length=200, blank=True, null=True)
    alternative_contact = models.CharField(max_length=200, blank=True, null=True)
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    state_id = models.BigIntegerField(null=True, blank=True)
    city_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    actual_start_time = models.TimeField(null=True, blank=True)
    actual_end_time = models.TimeField(null=True, blank=True)
    actual_duration = models.BigIntegerField(blank=True, null=True)
    completed_task_details = JSONField(null=True, blank=True)
    sa_GIS_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return str(self.id_string) + " - " +str(self.consumer_service_contract_detail_id)

    def __unicode__(self):
        return self.id_string

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    
    @property
    def get_asset(self):
        asset = get_asset_by_id(self.asset_id)
        return {
            "name":asset.name,
            "id_string":asset.id_string
        }

    @property
    def get_service(self):
        work_order_template = get_work_order_master_by_id(self.work_order_master_id)
        return work_order_template
       
    
    @property
    def get_status(self):
        return get_service_appointment_status_by_id(self.status_id)

    @property
    def get_state(self):
        return get_state_by_id(self.state_id)

    @property
    def get_area(self):
        return get_area_by_id(self.area_id)
    
    @property
    def get_sub_area(self):
        return get_sub_area_by_id(self.sub_area_id)

    @property
    def get_city(self):
        return get_city_by_id(self.city_id)

    @property
    def get_consumer_service_contract_detail_id(self):
        consumer_service_contract_detail = get_consumer_service_contract_detail_by_id(self.consumer_service_contract_detail_id)
        return consumer_service_contract_detail
    
    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            print("======",previous_state)
            print("======",next_state)
            # perform_events(next_state, self, TRANSITION_CONFIGURATION_DICT["REGISTRATION"])
            # perform_signals(next_state, self)
            self.save()
        except Exception as e:
            raise CustomAPIException("Service Appointment transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)

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
