import collections

from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.asset.models.asset_master import get_asset_by_id_string
from v1.work_order.models.work_order_master import get_work_order_master_by_id_string
from v1.work_order.models.service_appointment_status import get_service_appointment_status_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat
from rest_framework import status
from v1.commonapp.models.sub_module import get_sub_module_by_key
# from v1.commonapp.models.service_request_type import get_service_type_by_id_string
# from v1.commonapp.models.service_request_sub_type import get_service_sub_type_by_id_string
from v1.utility.models.utility_work_order_type import get_utility_work_order_type_by_id_string
from v1.utility.models.utility_work_order_sub_type import get_utility_work_order_sub_type_by_id_string
from v1.work_order.models.service_appointments import get_service_appointment_by_id_string
from master.models import get_user_by_id_string
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string, CONSUMER_DICT, get_consumer_service_contract_detail_by_id
from v1.meter_data_management.views.common_function import set_meter_validated_data
from v1.consumer.views.common_functions import set_consumer_service_contract_detail_validated_data

def set_work_order_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "utility_work_order_type_id" in validated_data:
        utility_work_order_type = get_utility_work_order_type_by_id_string(validated_data["utility_work_order_type_id"])
        if utility_work_order_type:
            validated_data["utility_work_order_type_id"] = utility_work_order_type.id
        else:
            raise CustomAPIException("Utility Work Order Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "utility_work_order_sub_type_id" in validated_data:
        utility_work_order_sub_type = get_utility_work_order_sub_type_by_id_string(validated_data["utility_work_order_sub_type_id"])
        if utility_work_order_sub_type:
            validated_data["utility_work_order_sub_type_id"] = utility_work_order_sub_type.id
        else:
            raise CustomAPIException("Utility Work Order Sub Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_service_appointment_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        if state:
            validated_data["state_id"] = state.id
        else:
            raise CustomAPIException("State not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        if sub_area:
            validated_data["sub_area_id"] = sub_area.id
        else:
            raise CustomAPIException("Sub area not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "premise_id" in validated_data:
        premise = get_premise_by_id_string(validated_data["premise_id"])
        if premise:
            validated_data["premise_id"] = premise.id
        else:
            raise CustomAPIException("Premise not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "consumer_id" in validated_data:
        consumers = get_consumer_by_id_string(validated_data["consumer_id"])
        if consumers:
            validated_data["consumer_id"] = consumers.id
        else:
            raise CustomAPIException("Consumer not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "asset_id" in validated_data:
        asset = get_asset_by_id_string(validated_data["asset_id"])
        if asset:
            validated_data["asset_id"] = asset.id
        else:
            raise CustomAPIException("Asset not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "work_order_master_id" in validated_data:
        service = get_work_order_master_by_id_string(validated_data["work_order_master_id"])
        if service:
            validated_data["work_order_master_id"] = service.id
        else:
            raise CustomAPIException("Service not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "status_id" in validated_data:
        status_obj = get_service_appointment_status_by_id_string(validated_data["status_id"])
        if status:
            validated_data["status_id"] = status_obj.id
        else:
            raise CustomAPIException("status not found.", status_code=status.HTTP_404_NOT_FOUND)
    
    if "consumer_service_contract_detail_id" in validated_data:
        consumer_service_contract_detail_obj = get_consumer_service_contract_detail_by_id_string(validated_data["consumer_service_contract_detail_id"])
        if consumer_service_contract_detail_obj:
            validated_data["consumer_service_contract_detail_id"]=consumer_service_contract_detail_obj.id
        else:
            raise CustomAPIException("consumer service contract detail not found.", status_code=status.HTTP_404_NOT_FOUND) 

    return validated_data

def set_schedule_appointment_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)

    return validated_data

# Function for generating service appointment number according to utility
def generate_service_appointment_no(service_appointment):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=service_appointment.tenant,
                                                            utility=service_appointment.utility,
                                                            sub_module_id=get_sub_module_by_key("DISPATCHER"))
        if format_obj.is_prefix:
            sa_number = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            sa_number = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return sa_number
    except Exception as e:
        raise CustomAPIException("sa_number no generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def set_service_assignment_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "sa_id" in validated_data:
        service_appointment = get_service_appointment_by_id_string(validated_data["sa_id"])
        if service_appointment:
            validated_data["sa_id"] = service_appointment.id
        else:
            raise CustomAPIException("Service Appointment not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "status_id" in validated_data:
        status_obj = get_service_appointment_status_by_id_string(validated_data["status_id"])
        if status:
            validated_data["status_id"] = status_obj.id
        else:
            raise CustomAPIException("status not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_service_appointment_data(work_order, consumer):
    try:
        od = collections.OrderedDict()
        od['work_order_master_id'] = work_order.id
        od['tenant_id'] = consumer.tenant.id
        od['utility_id'] = consumer.utility.id
        od['consumer_id'] = consumer.id
        return od
    except Exception as e:
        raise CustomAPIException("Error in setting service_appointment_data",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def set_meter_install_data(service_appointment_obj):
    try:
        meter = collections.OrderedDict()
        mobile_data = service_appointment_obj.completed_task_details
        validated_data = set_meter_validated_data(mobile_data)
        meter['tenant_id'] = service_appointment_obj.tenant.id
        meter['utility_id'] = service_appointment_obj.utility.id
        meter['utility_product_id'] = validated_data['utility_product_id']
        meter['route_id'] = validated_data['route_id']
        meter['premise_id'] = validated_data['premise_id']
        meter['meter_no'] = validated_data['meter_no']
        meter['meter_make_id'] = validated_data['meter_make_id']
        return meter
    except Exception as e:
        print(e)
        raise CustomAPIException("Error in setting meter data",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def set_consumer_service_contract_data(appointment_obj,meter_obj):
    try:
        contract_obj = collections.OrderedDict()
        con_contract = get_consumer_service_contract_detail_by_id(appointment_obj.consumer_service_contract_detail_id)
        if con_contract:
            con_contract.change_state(CONSUMER_DICT["CONNECTED"])
        contract_obj['meter_id'] = meter_obj.id
        return contract_obj
    except Exception as e:
        print(e)
        raise CustomAPIException("Error in setting meter data",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)