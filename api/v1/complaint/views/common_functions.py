from rest_framework import status

from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.complaint.models.complaint_status import get_complaint_status_by_id_string
from v1.complaint.models.complaint_sub_type import get_complaint_sub_type_by_id_string
from v1.complaint.models.complaint_type import get_complaint_type_by_id_string
from v1.complaint.models.consumer_complaint_master import get_consumer_complaint_master_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string


# Function for converting id_strings to id's
def set_complaint_validated_data(validated_data):
    if "consumer_complaint_master_id" in validated_data:
        complaint = get_consumer_complaint_master_by_id_string(validated_data["consumer_complaint_master_id"])
        if complaint:
            validated_data["consumer_complaint_master_id"] = complaint.id
        else:
            raise CustomAPIException("Complaint type not found.", status.HTTP_404_NOT_FOUND)
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
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=consumer.tenant, utility=consumer.utility,
                                                            sub_module_id=get_sub_module_by_key("COMPLAINT"))
        if format_obj.is_prefix:
            complaint_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            complaint_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return complaint_no
    except Exception as e:
        print("#############3", e)
        raise CustomAPIException("Complaint no generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def set_complaint_type_validated_data(validated_data):
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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException("Utility Product not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_complaint_subtype_validated_data(validated_data):
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

    if "complaint_type_id" in validated_data:
        complaint_type = get_complaint_type_by_id_string(validated_data["complaint_type_id"])
        if complaint_type:
            validated_data["complaint_type_id"] = complaint_type.id
        else:
            raise CustomAPIException("Complaint Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_complaint_master_validated_data(validated_data):
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
    if "complaint_type_id" in validated_data:
        complaint_type = get_complaint_type_by_id_string(validated_data["complaint_type_id"])
        if complaint_type:
            validated_data["complaint_type_id"] = complaint_type.id
        else:
            raise CustomAPIException("Complaint Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "complaint_sub_type_id" in validated_data:
        complaint_sub_type = get_complaint_sub_type_by_id_string(validated_data["complaint_sub_type_id"])
        if complaint_sub_type:
            validated_data["complaint_sub_type_id"] = complaint_sub_type.id
        else:
            raise CustomAPIException("Complaint Sub Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
