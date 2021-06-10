__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to assign meter reading for validation
# Tables used: Meter Reading
# Author: Akshay
# Created on: 11/03/2021

from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.new_consumer_detail import NewConsumerDetail as NewConsumerDetailTbl
from v1.meter_data_management.models.validation_assignments import ValidationAssignment as ValidationAssignmentTbl


def validation_assignment():
    try:
        validation_assignment_obj = ValidationAssignmentTbl.objects.filter(is_active=True)

        for validation in validation_assignment_obj:
            # Validation Assignment To V1
            MeterReadingTbl.objects.filter(reading_status=0, is_assign_to_v1=False, is_active=True,
                                           is_duplicate=False, read_cycle_id=validation.read_cycle_id).update(
                validator_one_id=validation.validator1_id, is_assign_to_v1=True)
            # Validation Assignment To V2
            MeterReadingTbl.objects.filter(reading_status=1, is_assign_to_v2=False, is_active=True,
                                           is_duplicate=False, read_cycle_id=validation.read_cycle_id).update(
                validator_two_id=validation.validator2_id, is_assign_to_v2=True)
            # New Consumer Assignment
            NewConsumerDetailTbl.objects.filter(is_assigned=False, is_confirmed=False,
                                                read_cycle_id=validation.read_cycle_id).update(is_assigned=True)
            print("Validation Assignment Done")
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


validation_assignment()
