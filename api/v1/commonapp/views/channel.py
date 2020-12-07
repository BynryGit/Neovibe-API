import traceback
from rest_framework import generics
from v1.commonapp.serializers.country import CountrySerializer
from v1.tenant.models.tenant_country import TenantCountry as TenantCountryTbl
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
import traceback
from v1.commonapp.serializers.region import TenantRegionSerializer
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.serializers.region import TenantRegionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.serializers.consumer import ConsumerSerializer, ConsumerViewSerializer
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.service.models.consumer_services import get_consumer_services_by_consumer_no
from v1.service.serializers.service import ServiceDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.serializers.channel import ChannelListSerializer,ChannelViewSerializer,ChannelSerializer
from v1.commonapp.models.channel import Channel as ChannelModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/channel/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Channel list
# Usage: API will fetch all Channel list
# Tables used: Channel
# Author: Chinmay
# Created on: 27/11/2020


class ChannelList(generics.ListAPIView):
    try:
        serializer_class = ChannelListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = ChannelModel.objects.all()
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

# API Header
# API end Point: api/v1/utility/city
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Channel post
# Usage: API will Post the Channel
# Tables used: Channel
# Author: Chinmay
# Created on: 30/11/2020
class Channel(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ChannelSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                channel_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ChannelViewSerializer(instance=channel_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)