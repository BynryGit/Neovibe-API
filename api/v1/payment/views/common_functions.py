__author__ = "Rohan"

from rest_framework import status

from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.payment.models.payment_channel import get_payment_channel_by_id_string
from v1.payment.models.payment_mode import get_payment_mode_by_id_string
from v1.payment.models.payment_source import get_payment_source_by_id_string
from v1.payment.models.payment_sub_type import get_payment_sub_type_by_id_string
from v1.payment.models.payment_type import get_payment_type_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_payment_channel import get_utility_payment_channel_by_id_string
from v1.utility.models.utility_payment_mode import get_utility_payment_mode_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.utility.models.utility_payment_subtype import get_utility_payment_subtype_by_id_string
from v1.utility.models.utility_payment_type import get_utility_payment_type_by_id_string


# Function for converting request data id strings to id's
def set_payment_validated_data(validated_data):
    if "utility" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility"])
        if utility:
            validated_data["utility"] = utility
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "payment_type_id" in validated_data:
        payment_type = get_utility_payment_type_by_id_string(validated_data["payment_type_id"])
        if payment_type:
            validated_data["payment_type_id"] = payment_type.id
        else:
            raise CustomAPIException("Payment type not found.", status.HTTP_404_NOT_FOUND)
    # if "payment_sub_type_id" in validated_data:
    #     payment_sub_type = get_payment_sub_type_by_id_string(validated_data["payment_sub_type_id"])
    #     if payment_sub_type:
    #         validated_data["payment_sub_type_id"] = payment_sub_type.id
    #     else:
    #         raise CustomAPIException("Payment sub type not found.", status.HTTP_404_NOT_FOUND)
    if "payment_mode_id" in validated_data:
        payment_mode = get_utility_payment_mode_by_id_string(validated_data["payment_mode_id"])
        if payment_mode:
            validated_data["payment_mode_id"] = payment_mode.id
        else:
            raise CustomAPIException("Payment mode not found.", status.HTTP_404_NOT_FOUND)
    if "payment_channel_id" in validated_data:
        payment_channel = get_utility_payment_channel_by_id_string(validated_data["payment_channel_id"])
        if payment_channel:
            validated_data["payment_channel_id"] = payment_channel.id
        else:
            raise CustomAPIException("Payment channel not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating payment receipt number according to utility
def generate_receipt_no(payment):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=payment.tenant, utility=payment.utility,
                                                            sub_module_id=get_sub_module_by_key("PAYMENT").id)
        if format_obj.is_prefix:
            receipt_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            receipt_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return receipt_no
    except Exception as e:
        raise CustomAPIException("Receipt no generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Function for converting request data id strings to id's
def set_payment_transaction_validated_data(validated_data):
    if "transaction_type_id" in validated_data:
        payment_type = get_utility_payment_type_by_id_string(validated_data["transaction_type_id"])
        if payment_type:
            validated_data["transaction_type_id"] = payment_type.id
        else:
            raise CustomAPIException("Payment type not found.", status.HTTP_404_NOT_FOUND)
    if "transaction_sub_type_id" in validated_data:
        payment_sub_type = get_utility_payment_subtype_by_id_string(validated_data["transaction_sub_type_id"])
        if payment_sub_type:
            validated_data["transaction_sub_type_id"] = payment_sub_type.id
        else:
            raise CustomAPIException("Payment sub type not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


def set_payment_type_validated_data(validated_data):
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
    if "payment_type_id" in validated_data:
        payment_type = get_payment_type_by_id_string(validated_data["payment_type_id"])
        if payment_type:
            validated_data["payment_type_id"] = payment_type.id
        else:
            raise CustomAPIException("Payment Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_payment_subtype_validated_data(validated_data):
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

    if "payment_type_id" in validated_data:
        payment_type = get_utility_payment_type_by_id_string(validated_data["payment_type_id"])
        if payment_type:
            validated_data["payment_type_id"] = payment_type.id
        else:
            raise CustomAPIException("Payment Type not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "payment_subtype_id" in validated_data:
        payment_subtype = get_payment_sub_type_by_id_string(validated_data["payment_subtype_id"])
        if payment_subtype:
            validated_data["payment_subtype_id"] = payment_subtype.id
        else:
            raise CustomAPIException("Payment SubType not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_payment_mode_validated_data(validated_data):
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

    if "payment_mode_id" in validated_data:
        payment_mode = get_payment_mode_by_id_string(validated_data["payment_mode_id"])
        if payment_mode:
            validated_data["payment_mode_id"] = payment_mode.id
        else:
            raise CustomAPIException("Payment Mode not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
