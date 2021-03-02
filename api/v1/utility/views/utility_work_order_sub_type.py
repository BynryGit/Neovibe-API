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
from v1.utility.serializers.utility_work_order_sub_type import UtilityWorkOrderSubTypeListSerializer
from v1.utility.models.utility_work_order_sub_type import UtilityWorkOrderSubType as UtilityWorkOrderSubTypeModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_filter_backend import CustomFilter
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/:id_string/work-order-sub-type/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Work Order Sub Type list
# Usage: API will fetch all Work Order Sub Type list
# Tables used: WorkOrderSubType
# Author: Chinmay
# Created on: 3/1/2021

class UtilityWorkOrderSubTypeList(generics.ListAPIView):
    try:
        serializer_class = UtilityWorkOrderSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityWorkOrderSubTypeModel.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Work Order Sub Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')
