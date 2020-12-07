from v1.commonapp.serializers.region import TenantRegionSerializer
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.serializers.utility_channel import UtilityChannelListSerializer
from v1.utility.models.utility_channel import UtilityChannel as UtilityChannelModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.channel import get_channel_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/utility/:id_string/channel/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Channel list
# Usage: API will fetch all region list
# Tables used: Channel
# Author: Chinmay
# Created on: 30/11/2020

class UtilityChannelList(generics.ListAPIView):
    try:
        serializer_class = UtilityChannelListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityChannelModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Channel not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')