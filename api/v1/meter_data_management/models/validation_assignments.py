__author__ = "chinmay"

# Table Header
# Module: Admin | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : ValidationAssignment
# Description : It is ValidationAssignment table. This table will save all the Validation Assignments.
# Frequency of data changes : Low
# Sample table :
# Reference Table : None
# Author : Chinmay Pathak
# Creation Date : 26/02/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from master.models import get_user_by_id


# Create ValidationAssignment Table Start

class ValidationAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    read_cycle_id = models.BigIntegerField(null=True, blank=True)
    validator1_id = models.BigIntegerField(null=True, blank=True)
    validator2_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name

    @property
    def get_read_cycle(self):
        read_cycle = get_read_cycle_by_id(self.read_cycle_id)
        return read_cycle

    @property
    def get_validator_1(self):
        validator_1 = get_user_by_id(self.validator1_id)
        return validator_1

    @property
    def get_validator_2(self):
        validator_2 = get_user_by_id(self.validator2_id)
        print("BBBBBBBBBB",validator_2)
        return validator_2


# Create ValidationAssignment Table end


def get_validation_assignment_by_id(id):
    try:
        return ValidationAssignment.objects.get(id=id, is_active=True)
    except:
        return False


def get_validation_assignment_by_id_string(id_string):
    try:
        return ValidationAssignment.objects.get(id_string=id_string, is_active=True)
    except:
        return False
