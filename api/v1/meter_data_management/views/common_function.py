__author__ = "aki"

from api.messages import *
from rest_framework import status
from master.models import get_user_by_id_string
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id_string
from v1.meter_data_management.models.route import get_route_by_id_string
from v1.meter_data_management.models.schedule_log import get_schedule_log_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.division import get_division_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.meter_data_management.models.consumer_detail import get_consumer_detail_by_id_string
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id_string
from v1.commonapp.models.meter_status import get_meter_status_by_id_string, get_meter_status_by_name
from v1.meter_data_management.models.reader_status import get_reader_status_by_id_string, get_reader_status_by_name
from v1.meter_data_management.models.meter_make import get_meter_make_by_id_string

def set_schedule_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "recurring_id" in validated_data:
        recurring = get_global_lookup_by_id_string(validated_data["recurring_id"])
        if recurring:
            validated_data["recurring_id"] = recurring.id
        else:
            raise CustomAPIException(IS_RECCURING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

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
    else:
        validated_data["frequency_id"] = None

    if "repeat_every_id" in validated_data:
        repeat_every = get_global_lookup_by_id_string(validated_data["repeat_every_id"])
        if repeat_every:
            validated_data["repeat_every_id"] = repeat_every.id
        else:
            raise CustomAPIException(REPEAT_FREQUENCY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    else:
        validated_data["repeat_every_id"] = None

    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException(UTILITY_PRODUCT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "occurs_on" in validated_data:
        pass
    else:
        validated_data["occurs_on"] = []

    if "end_date" in validated_data:
        pass
    else:
        validated_data["end_date"] = None

    if "cron_expression" in validated_data:
        pass
    else:
        validated_data["cron_expression"] = None

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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException(UTILITY_PRODUCT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException(UTILITY_PRODUCT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_meter_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "route_id" in validated_data:
        route = get_route_by_id_string(validated_data["route_id"])
        if route:
            validated_data["route_id"] = route.id
        else:
            raise CustomAPIException(ROUTE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "premise_id" in validated_data:
        premise = get_premise_by_id_string(validated_data["premise_id"])
        if premise:
            validated_data["premise_id"] = premise.id
        else:
            raise CustomAPIException(PREMISE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "meter_make_id" in validated_data:
        meter_make = get_meter_make_by_id_string(validated_data["meter_make_id"])
        if meter_make:
            validated_data["meter_make_id"] = meter_make.id
        else:
            raise CustomAPIException(METER_MAKE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "meter_type_id" in validated_data:
        meter_type = get_global_lookup_by_id_string(validated_data["meter_type_id"])
        if meter_type:
            validated_data["meter_type_id"] = meter_type.id
        else:
            raise CustomAPIException(METER_TYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException(UTILITY_PRODUCT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "install_date" in validated_data:
        pass
    else:
        validated_data["install_date"] = None

    return validated_data


def set_smart_meter_validated_data(validated_data):
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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException(UTILITY_PRODUCT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_job_card_template_validated_data(validated_data):
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


def set_validation_assignment_validated_data(validated_data):
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
    if "validator1_id" in validated_data:
        validator1 = get_user_by_id_string(validated_data["validator1_id"])
        if validator1:
            validated_data["validator1_id"] = validator1.id
        else:
            raise CustomAPIException("Validator1 not found", status_code=status.HTTP_404_NOT_FOUND)
    if "validator2_id" in validated_data:
        validator2 = get_user_by_id_string(validated_data["validator2_id"])
        if validator2:
            validated_data["validator2_id"] = validator2.id
        else:
            raise CustomAPIException("Validator2 noy found", status_code=status.HTTP_404_NOT_FOUND)
    if "read_cycle_id" in validated_data:
        read_cycle = get_read_cycle_by_id_string(validated_data["read_cycle_id"])
        if read_cycle:
            validated_data["read_cycle_id"] = read_cycle.id
        else:
            raise CustomAPIException("Read Cycle not Found", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_reader_status_validated_data(validated_data):
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
    if "meter_status_id" in validated_data:
        meter_status = get_meter_status_by_id_string(validated_data["meter_status_id"])
        if meter_status:
            validated_data["meter_status_id"] = meter_status.id
        else:
            raise CustomAPIException("Meter Status Not Found", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_route_task_assignment_validated_data(validated_data):
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

    if "route_id" in validated_data:
        route = get_route_by_id_string(validated_data["route_id"])
        if route:
            validated_data["route_id"] = route.id
        else:
            raise CustomAPIException(ROUTE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "schedule_log_id" in validated_data:
        schedule_log = get_schedule_log_by_id_string(validated_data["schedule_log_id"])
        if schedule_log:
            validated_data["schedule_log_id"] = schedule_log.id
        else:
            raise CustomAPIException(SCHEDULE_LOG_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "meter_reader_id" in validated_data:
        meter_reader = get_user_by_id_string(validated_data["meter_reader_id"])
        if meter_reader:
            validated_data["meter_reader_id"] = meter_reader.id
        else:
            raise CustomAPIException(METER_READER_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_meter_reading_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            return None
    else:
        return None

    if "route_task_assignment_id" in validated_data:
        route_task_assignment_obj = get_route_task_assignment_by_id_string(
            validated_data['route_task_assignment_id'])
        if route_task_assignment_obj:
            validated_data["route_task_assignment_id"] = route_task_assignment_obj.id
        else:
            return None
    else:
        return None

    if "consumer_detail_id" in validated_data:
        consumer_detail_obj = get_consumer_detail_by_id_string(
            validated_data['consumer_detail_id'])
        if consumer_detail_obj:
            validated_data["consumer_detail_id"] = consumer_detail_obj.id
        else:
            return None
    else:
        return None

    if "meter_status_id" in validated_data:
        meter_status_obj = get_meter_status_by_id_string(
            validated_data['meter_status_id'])
        if meter_status_obj:
            validated_data["meter_status_id"] = meter_status_obj.id
        else:
            validated_data["meter_status_id"] = get_meter_status_by_name('Normal').id
    else:
        validated_data["meter_status_id"] = get_meter_status_by_name('Normal').id

    if "reader_status_id" in validated_data:
        reader_status_obj = get_reader_status_by_id_string(
            validated_data['reader_status_id'])
        if reader_status_obj:
            validated_data["reader_status_id"] = reader_status_obj.id
        else:
            validated_data["reader_status_id"] = get_reader_status_by_name('Normal').id
    else:
        validated_data["reader_status_id"] = get_reader_status_by_name('Normal').id

    return validated_data


def set_meter_reading_validation_revisit_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_meter_reading_validation_one_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "meter_status_v1_id" in validated_data:
        meter_status_obj = get_meter_status_by_id_string(
            validated_data['meter_status_v1_id'])
        if meter_status_obj:
            validated_data["meter_status_v1_id"] = meter_status_obj.id

    if "reader_status_v1_id" in validated_data:
        reader_status_obj = get_reader_status_by_id_string(
            validated_data['reader_status_v1_id'])
        if reader_status_obj:
            validated_data["reader_status_v1_id"] = reader_status_obj.id

    return validated_data


def set_meter_reading_validation_two_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "meter_status_v2_id" in validated_data:
        meter_status_obj = get_meter_status_by_id_string(
            validated_data['meter_status_v2_id'])
        if meter_status_obj:
            validated_data["meter_status_v2_id"] = meter_status_obj.id

    if "reader_status_v2_id" in validated_data:
        reader_status_obj = get_reader_status_by_id_string(
            validated_data['reader_status_v2_id'])
        if reader_status_obj:
            validated_data["reader_status_v2_id"] = reader_status_obj.id

    return validated_data


def set_upload_route_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "schedule_log_id" in validated_data:
        schedule_log = get_schedule_log_by_id_string(validated_data["schedule_log_id"])
        if schedule_log:
            validated_data["schedule_log_id"] = schedule_log.id
        else:
            raise CustomAPIException(SCHEDULE_LOG_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "read_cycle_id" in validated_data:
        read_cycle = get_read_cycle_by_id_string(validated_data["read_cycle_id"])
        if read_cycle:
            validated_data["read_cycle_id"] = read_cycle.id
        else:
            raise CustomAPIException(READ_CYCLE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "route_id" in validated_data:
        route = get_route_by_id_string(validated_data["route_id"])
        if route:
            validated_data["route_id"] = route.id
        else:
            raise CustomAPIException(ROUTE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    return validated_data
