# table header
# module: Work Order | sub-module -
# Table Type : Main
# Table Name : scheduled appointment
# Description : It is a master table that stores scheduled appointment.
# Frequency of data changes : high
# Sample table :
# Reference Table :scheduledappointment
# Author : Priyanka 
# Creation Date :08/02/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database

from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.views.custom_exception import ObjectNotFoundException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.region import get_region_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.city import get_city_by_id
from django.contrib.postgres.fields import JSONField
from master.models import get_user_by_id
# Create ScheduledAppointment table start


class ScheduledAppointment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    appointments = JSONField()
    user_id = models.BigIntegerField(null=True, blank=True)
    assignment_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.user_id)

    def __unicode__(self):
        return self.user_id

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility
    
    @property
    def get_user(self):
        user_val = get_user_by_id(self.user_id)
        return {
            "first_name":user_val.first_name,
            "last_name":user_val.last_name,
            "id_string":user_val.id_string,
            "email":user_val.email,
            "phone_mobile":user_val.phone_mobile
        }

# Create ScheduledAppointment table end

def get_scheduled_appointment_by_tenant_id_string(id_string):
    return ScheduledAppointment.objects.filter(tenant__id_string=id_string)


def get_scheduled_appointment_by_utility_id_string(id_string):
    return ScheduledAppointment.objects.filter(utility__id_string=id_string)


def get_scheduled_appointment_by_id(id):
    try:
        return ScheduledAppointment.objects.get(id=id)
    except:
        return False


def get_scheduled_appointment_by_id_string(id_string):
    try:
        return ScheduledAppointment.objects.get(id_string=id_string)
    except:
        return False
