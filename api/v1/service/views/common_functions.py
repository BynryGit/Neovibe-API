from rest_framework import status
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.service_status import get_service_status_by_id_string
from v1.consumer.models.service_sub_type import get_service_sub_type_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT


# Function for converting id_strings to id's
def set_service_validated_data(validated_data):
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
    if "service_status_id" in validated_data:
        service_status = get_service_status_by_id_string(validated_data["service_status_id"])
        if service_status:
            validated_data["service_status_id"] = service_status.id
        else:
            raise CustomAPIException("Service status not found.", status.HTTP_404_NOT_FOUND)
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