from rest_framework import status
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.complaint.models.complaint_status import get_complaint_status_by_id_string
from v1.complaint.models.complaint_sub_type import get_complaint_sub_type_by_id_string
from v1.complaint.models.complaint_type import get_complaint_type_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT


# Function for converting id_strings to id's
def set_complaint_validated_data(validated_data):
    if "complaint_type_id" in validated_data:
        complaint_type = get_complaint_type_by_id_string(validated_data["complaint_type_id"])
        if complaint_type:
            validated_data["complaint_type_id"] = complaint_type.id
        else:
            raise CustomAPIException("Complaint type not found.", status.HTTP_404_NOT_FOUND)
    if "complaint_sub_type_id" in validated_data:
        complaint_sub_type = get_complaint_sub_type_by_id_string(validated_data["complaint_sub_type_id"])
        if complaint_sub_type:
            validated_data["complaint_sub_type_id"] = complaint_sub_type.id
        else:
            raise CustomAPIException("Complaint sub type not found.", status.HTTP_404_NOT_FOUND)
    if "complaint_status_id" in validated_data:
        complaint_status = get_complaint_status_by_id_string(validated_data["complaint_status_id"])
        if complaint_status:
            validated_data["complaint_status_id"] = complaint_status.id
        else:
            raise CustomAPIException("Complaint status not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating complaint number aaccording to utility
def generate_complaint_no(consumer):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant = consumer.tenant, utility = consumer.utility,
                                                            item = UTILITY_SERVICE_NUMBER_ITEM_DICT['COMPLAINT'])
        if format_obj.is_prefix == True:
            complaint_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            complaint_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return complaint_no
    except Exception as e:
        raise CustomAPIException("Complaint no generation failed.",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)