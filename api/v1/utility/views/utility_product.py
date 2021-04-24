
from rest_framework import status, generics
from api.messages import *
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.utility.serializers.utility_product import UtilityProductListSerializer
from v1.utility.models.utility_product import UtilityProduct as UtilityProductModel
from v1.utility.models.utility_master import get_utility_by_id_string
from api.constants import *
from v1.commonapp.views.custom_filter_backend import CustomFilter


# API Header
# API end Point: api/v1/:id_string/product/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: products list
# Usage: API will fetch all product list
# Tables used: UtilityProduct
# Author: Chinmay
# Created on: 6/1/2021

class UtilityProductList(generics.ListAPIView):
    try:
        serializer_class = UtilityProductListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityProductModel.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Product Not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')
