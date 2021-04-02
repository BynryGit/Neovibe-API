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
from v1.meter_data_management.models.validation_assignments import ValidationAssignment as ValidationAssignmentTbl


def validation_assignment():
    try:
        validation_assignment_obj = ValidationAssignmentTbl.objects.filter(is_active=True)
        for validation in validation_assignment_obj:
            meter_reading_obj = MeterReadingTbl.objects.filter(reading_status=0, is_assign_to_v1=False, is_active=True,
                                                               is_duplicate=False, read_cycle_id=validation.read_cycle_id)
            for meter_reading in meter_reading_obj:
                meter_reading.validator_one_id = validation.validator1_id
                meter_reading.is_assign_to_v1 = True
                meter_reading.save()

            meter_reading_obj = MeterReadingTbl.objects.filter(reading_status=1, is_assign_to_v2=False, is_active=True,
                                                               is_duplicate=False, read_cycle_id=validation.read_cycle_id)
            for meter_reading in meter_reading_obj:
                meter_reading.validator_two_id = validation.validator2_id
                meter_reading.is_assign_to_v2 = True
                meter_reading.save()
            print("Validation Assignment Done")
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


validation_assignment()
