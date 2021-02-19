from rest_framework import status
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.service_status import get_service_status_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT


# Function for converting id_strings to id's
def set_service_validated_data(validated_data):
    if "service_status_id" in validated_data:
        service_status = get_service_status_by_id_string(validated_data["service_status_id"])
        if service_status:
            validated_data["service_status_id"] = service_status.id
        else:
            raise CustomAPIException("Service status not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_service_master_validated_data(validated_data):
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
    if "service_type_id" in validated_data:
        service_type = get_service_type_by_id_string(validated_data["service_type_id"])
        if service_type:
            validated_data["service_type_id"] = service_type.id
        else:
            raise CustomAPIException("Service type not found.", status.HTTP_404_NOT_FOUND)
    if "service_sub_type_id" in validated_data:
        service_sub_type = get_service_sub_type_by_id_string(validated_data["service_sub_type_id"])
        if service_sub_type:
            validated_data["service_sub_type_id"] = service_sub_type.id
        else:
            raise CustomAPIException("Service sub type not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_service_master_validated_data(validated_data):
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
    if "service_type_id" in validated_data:
        service_type = get_service_type_by_id_string(validated_data["service_type_id"])
        if service_type:
            validated_data["service_type_id"] = service_type.id
        else:
            raise CustomAPIException("Service type not found.", status.HTTP_404_NOT_FOUND)
    if "service_sub_type_id" in validated_data:
        service_sub_type = get_service_sub_type_by_id_string(validated_data["service_sub_type_id"])
        if service_sub_type:
            validated_data["service_sub_type_id"] = service_sub_type.id
        else:
            raise CustomAPIException("Service sub type not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating service number aaccording to utility
def generate_service_no(service):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant = service.tenant, utility = service.utility,
                                                            item = UTILITY_SERVICE_NUMBER_ITEM_DICT['SERVICE'])
        if format_obj.is_prefix == True:
            service_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            service_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return service_no
    except Exception as e:
        raise CustomAPIException("Service no generation failed.",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)