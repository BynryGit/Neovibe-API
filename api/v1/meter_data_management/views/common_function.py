__author__ = "aki"

from rest_framework import status
from api.messages import CITY_NOT_FOUND, TENANT_NOT_FOUND, UTILITY_NOT_FOUND, FREQUENCY_NOT_FOUND, DIVISION_NOT_FOUND, \
    AREA_NOT_FOUND, SUBAREA_NOT_FOUND, ZONE_NOT_FOUND
from api.messages import *
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.division import get_division_by_id_string


def set_schedule_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "read_cycle_id" in validated_data:
        read_cycle = get_read_cycle_by_id_string(validated_data["read_cycle_id"])
        if read_cycle:
            validated_data["read_cycle_id"] = read_cycle.id
        else:
            raise CustomAPIException(READ_CYCLE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "activity_type_id" in validated_data:
        activity = get_global_lookup_by_id_string(validated_data["activity_type_id"])
        if activity:
            validated_data["activity_type_id"] = activity.id
        else:
            raise CustomAPIException(ACTIVITY_TYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "frequency_id" in validated_data:
        frequency = get_global_lookup_by_id_string(validated_data["frequency_id"])
        if frequency:
            validated_data["frequency_id"] = frequency.id
        else:
            raise CustomAPIException(FREQUENCY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "repeat_every_id" in validated_data:
        repeat_every = get_global_lookup_by_id_string(validated_data["repeat_every_id"])
        if repeat_every:
            validated_data["repeat_every_id"] = repeat_every.id
        else:
            raise CustomAPIException(REPEAT_FREQUENCY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_read_cycle_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException(TENANT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException(CITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "zone_id" in validated_data:
        zone = get_zone_by_id_string(validated_data["zone_id"])
        if zone:
            validated_data["zone_id"] = zone.id
        else:
            raise CustomAPIException(ZONE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "division_id" in validated_data:
        division = get_division_by_id_string(validated_data["division_id"])
        if division:
            validated_data["division_id"] = division.id
        else:
            raise CustomAPIException(DIVISION_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException(AREA_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "subarea_id" in validated_data:
        subarea = get_sub_area_by_id_string(validated_data["subarea_id"])
        if subarea:
            validated_data["subarea_id"] = subarea.id
        else:
            raise CustomAPIException(SUBAREA_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_route_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException(TENANT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
