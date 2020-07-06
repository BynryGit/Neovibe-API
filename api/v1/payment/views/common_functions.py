from rest_framework import status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.payment.models.payment_channel import get_payment_channel_by_id_string
from v1.payment.models.payment_mode import get_payment_mode_by_id_string
from v1.payment.models.payment_source import get_payment_source_by_id_string
from v1.payment.models.payment_sub_type import get_payment_sub_type_by_id_string
from v1.payment.models.payment_type import get_payment_type_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string


def set_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.",status_code=status.HTTP_404_NOT_FOUND)
    if "payment_type_id" in validated_data:
        payment_type = get_payment_type_by_id_string(validated_data["payment_type_id"])
        validated_data["payment_type_id"] = payment_type.id
    if "payment_sub_type_id" in validated_data:
        payment_sub_type = get_payment_sub_type_by_id_string(validated_data["payment_sub_type_id"])
        validated_data["payment_sub_type_id"] = payment_sub_type.id
    if "payment_mode_id" in validated_data:
        payment_mode = get_payment_mode_by_id_string(validated_data["payment_mode_id"])
        validated_data["payment_mode_id"] = payment_mode.id
    if "payment_channel_id" in validated_data:
        payment_channel = get_payment_channel_by_id_string(validated_data["payment_channel_id"])
        validated_data["payment_channel_id"] = payment_channel.id
    if "payment_source_id" in validated_data:
        payment_provider = get_payment_source_by_id_string(validated_data["payment_source_id"])
        validated_data["payment_source_id"] = payment_provider.id

    return validated_data