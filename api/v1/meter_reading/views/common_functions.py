from rest_framework import status
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_reading.models.activity_type import get_activity_type_by_id_string
from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id_string
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