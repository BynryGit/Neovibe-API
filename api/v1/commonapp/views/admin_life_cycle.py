from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.lifecycle import LifeCycle as LifeCycleTbl
from master.models import get_user_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.models.module import get_module_by_key
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.serializers.region import RegionSerializer, RegionViewSerializer, RegionListSerializer
from v1.commonapp.models.region import Region as RegionModel
from v1.commonapp.models.region import get_region_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/admin/life-cycle/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Admin cycle list
# Usage: API will fetch required data for meter life cycle list against filter and search
# Tables used: LifeCycle
# Author: Akshay
# Created on: 16/02/2021

class AdminLifeCycleList(generics.ListAPIView):
    try:
        serializer_class = LifeCycleListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('utility__id_string', 'object_id')
        ordering_fields = ('utility__id_string',)
        ordering = ('utility__id_string',)  # always give by default alphabetical order
        search_fields = ('utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    user_obj = get_user_by_id_string(self.kwargs['id_string'])
                    module = get_module_by_key("S&M")
                    sub_module = get_sub_module_by_key("S_AND_M_USER")
                    queryset = LifeCycleTbl.objects.filter(object_id=user_obj.id, module_id=module,
                                                           sub_module_id=sub_module, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Lifecycles not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'LOW', module='CONSUMER OPS', sub_module='METER DATA')
        raise APIException
