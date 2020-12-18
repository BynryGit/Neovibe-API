from rest_framework import status, generics
from v1.commonapp.common_functions import is_authorized, is_token_valid
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.serializers.utility_payment_type import UtilityPaymentTypeListSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_payment_type import UtilityPaymentType as UtilityPaymentTypeModel


# API Header
# API end Point: api/v1/utility/:id_string/payment/type/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Payment Type list
# Usage: API will fetch all Payment Type list
# Tables used: Utility Payment
# Author: Chinmay
# Created on: 3/12/2020
class UtilityPaymentTypeList(generics.ListAPIView):
    try:
        serializer_class = UtilityPaymentTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityPaymentTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Payment Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')
