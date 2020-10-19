__author__ = "Rohan"

from rest_framework import status
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.payment.models.payment_channel import get_payment_channel_by_id_string
from v1.payment.models.payment_mode import get_payment_mode_by_id_string
from v1.payment.models.payment_source import get_payment_source_by_id_string
from v1.payment.models.payment_sub_type import get_payment_sub_type_by_id_string
from v1.payment.models.payment_type import get_payment_type_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT


# Function for converting request data id strings to id's
def set_payment_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.",status_code=status.HTTP_404_NOT_FOUND)
    if "payment_type_id" in validated_data:
        payment_type = get_payment_type_by_id_string(validated_data["payment_type_id"])
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
        payment_mode = get_payment_mode_by_id_string(validated_data["payment_mode_id"])
        if payment_mode:
            validated_data["payment_mode_id"] = payment_mode.id
        else:
            raise CustomAPIException("Payment mode not found.", status.HTTP_404_NOT_FOUND)
    if "payment_channel_id" in validated_data:
        payment_channel = get_payment_channel_by_id_string(validated_data["payment_channel_id"])
        if payment_channel:
            validated_data["payment_channel_id"] = payment_channel.id
        else:
            raise CustomAPIException("Payment channel not found.", status.HTTP_404_NOT_FOUND)
    # if "payment_source_id" in validated_data:
    #     payment_provider = get_payment_source_by_id_string(validated_data["payment_source_id"])
    #     if payment_provider:
    #         validated_data["payment_source_id"] = payment_provider.id
    #     else:
    #         raise CustomAPIException("Payment souce not found.", status.HTTP_404_NOT_FOUND)

    return validated_data


# Function for generating payment receipt number aaccording to utility
def generate_receipt_no(payment):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant = payment.tenant, utility = payment.utility,
                                                            item = UTILITY_SERVICE_NUMBER_ITEM_DICT['PAYMENT'])
        if format_obj.is_prefix == True:
            receipt_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            receipt_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return receipt_no
    except Exception as e:
        raise CustomAPIException("Receipt no generation failed.",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Function for converting request data id strings to id's
def set_payment_transaction_validated_data(validated_data):
    if "transaction_type_id" in validated_data:
        payment_type = get_payment_type_by_id_string(validated_data["transaction_type_id"])
        if payment_type:
            validated_data["transaction_type_id"] = payment_type.id
        else:
            raise CustomAPIException("Payment type not found.", status.HTTP_404_NOT_FOUND)
    if "transaction_sub_type_id" in validated_data:
        payment_sub_type = get_payment_sub_type_by_id_string(validated_data["transaction_sub_type_id"])
        if payment_sub_type:
            validated_data["transaction_sub_type_id"] = payment_sub_type.id
        else:
            raise CustomAPIException("Payment sub type not found.", status.HTTP_404_NOT_FOUND)
    return validated_data