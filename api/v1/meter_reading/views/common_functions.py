__author__ = "aki"

from rest_framework import status

from master.models import get_user_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_reading.models.activity_type import get_activity_type_by_id_string
from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id_string
from v1.meter_reading.models.jobcard import get_jobcard_by_id_string
from v1.meter_reading.models.meter_reading import get_meter_reading_by_id_string
from v1.meter_reading.models.meter_status import get_meter_status_by_id_string
from v1.meter_reading.models.reader_status import get_reader_status_by_id_string
from v1.meter_reading.models.reading_status import get_reading_status_by_id_string
from v1.meter_reading.models.reading_taken_by import get_reading_taken_by_id_string
from v1.meter_reading.models.route import get_route_by_id_string
from v1.meter_reading.models.schedule_status import get_schedule_status_by_id_string
from v1.meter_reading.models.schedule_type import get_schedule_type_by_id_string


def set_schedule_validated_data(validated_data):
    if "schedule_type_id" in validated_data:
        schedule_type = get_schedule_type_by_id_string(validated_data["schedule_type_id"])
        if schedule_type:
            validated_data["schedule_type_id"] = schedule_type.id
        else:
            raise CustomAPIException("Schedule type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "activity_type_id" in validated_data:
        activity_type = get_activity_type_by_id_string(validated_data["activity_type_id"])
        if activity_type:
            validated_data["activity_type_id"] = activity_type.id
        else:
            raise CustomAPIException("Activity type not found.", status.HTTP_404_NOT_FOUND)
    if "bill_cycle_id" in validated_data:
        bill_cycle = get_bill_cycle_by_id_string(validated_data["bill_cycle_id"])
        if bill_cycle:
            validated_data["bill_cycle_id"] = bill_cycle.id
        else:
            raise CustomAPIException("Bill cycle type not found.", status.HTTP_404_NOT_FOUND)
    if "schedule_status_id" in validated_data:
        schedule_status = get_schedule_status_by_id_string(validated_data["schedule_status_id"])
        if schedule_status:
            validated_data["schedule_status_id"] = schedule_status.id
        else:
            raise CustomAPIException("Schedule status type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_meter_reading_validated_data(validated_data):
    if "bill_cycle_id" in validated_data:
        bill_cycle = get_bill_cycle_by_id_string(validated_data["bill_cycle_id"])
        validated_data["bill_cycle_id"] = bill_cycle.id
    if "route_id" in validated_data:
        route = get_route_by_id_string(validated_data["route_id"])
        validated_data["route_id"] = route.id
    if "jobcard_id" in validated_data:
        jobcard = get_jobcard_by_id_string(validated_data["jobcard_id"])
        validated_data["jobcard_id"] = jobcard.id
    if "reading_status_id" in validated_data:
        reading_status = get_reading_status_by_id_string(validated_data["reading_status_id"])
        validated_data["reading_status_id"] = reading_status.id
    if "meter_status_id" in validated_data:
        meter_status = get_meter_status_by_id_string(validated_data["meter_status_id"])
        validated_data["meter_status_id"] = meter_status.id
    if "reader_status_id" in validated_data:
        reader_status = get_reader_status_by_id_string(validated_data["reader_status_id"])
        validated_data["reader_status_id"] = reader_status.id
    if "reading_taken_by_id" in validated_data:
        reading_taken_by = get_reading_taken_by_id_string(validated_data["reading_taken_by_id"])
        validated_data["reading_taken_by_id"] = reading_taken_by.id
    return validated_data


def set_route_assignment_validated_data(validated_data):
    if "meter_reader_id" in validated_data:
        meter_reader = get_user_by_id_string(validated_data["meter_reader_id"])
        validated_data["meter_reader_id"] = meter_reader.id
    return validated_data


def set_validation_validated_data(validated_data):
    if "bill_cycle_id" in validated_data:
        bill_cycle = get_bill_cycle_by_id_string(validated_data["bill_cycle_id"])
        validated_data["bill_cycle_id"] = bill_cycle.id
    if "route_id" in validated_data:
        route = get_route_by_id_string(validated_data["route_id"])
        validated_data["route_id"] = route.id
    if "meter_reading_id" in validated_data:
        meter_reading = get_meter_reading_by_id_string(validated_data["meter_reading_id"])
        validated_data["meter_reading_id"] = meter_reading.id
    if "validator_id" in validated_data:
        validator = get_user_by_id_string(validated_data["validator_id"])
        validated_data["validator_id"] = validator.id
    return validated_data
