__author__ = "aki"

from rest_framework import status
from api.messages import *
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_master import get_utility_by_id_string


def set_schedule_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    # if "read_cycle_id" in validated_data:
    #     read_cycle = get_read_cycle_by_id_string(validated_data["read_cycle_id"])
    #     if read_cycle:
    #         validated_data["read_cycle_id"] = read_cycle.id
    #     else:
    #         raise CustomAPIException(READ_CYCLE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "frequency_id" in validated_data:
        frequency = get_global_lookup_by_id_string(validated_data["frequency_id"])
        if frequency:
            validated_data["frequency_id"] = frequency.id
        else:
            raise CustomAPIException(FREQUENCY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
