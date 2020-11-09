__author__ = "aki"

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
#from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
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
from v1.commonapp.serializers.region import RegionSerializer,RegionViewSerializer,RegionListSerializer
from v1.commonapp.models.region import Region as RegionModel
# API Header
# API end Point: api/v1/regions
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: regions list
# Usage: API will fetch all region list
# Tables used: TenantRegion
# Author: Akshay
# Created on: 15/05/2020


# class RegionList(generics.ListAPIView):

#     def get(self, request):
#         try:
#             # Checking authentication start
#             if is_token_valid(request.headers['token']):
#                 # payload = get_payload(request.headers['token'])
#                 # user = get_user(payload['id_string'])
#                 # Checking authentication end

#                 # Checking authorization start
#                 if is_authorized():
#                 # Checking authorization end

#                     regions_obj = TenantRegionTbl.objects.filter(is_active=True)
#                     if regions_obj:
#                         serializer = TenantRegionSerializer(regions_obj, many=True)
#                         return Response({
#                             STATE: SUCCESS,
#                             RESULTS: serializer.data,
#                         }, status=status.HTTP_200_OK)
#                     else:
#                         return Response({
#                             STATE: ERROR,
#                         }, status=status.HTTP_404_NOT_FOUND)
#                 else:
#                     return Response({
#                         STATE: ERROR,
#                     }, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as ex:
#             logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
#             return Response({
#                 STATE: EXCEPTION,
#                 ERROR: str(traceback.print_exc(ex))
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegionList(generics.ListAPIView):
    try:
        serializer_class = RegionListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = RegionModel.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Region not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Commonapp', sub_module = 'Commonapp')

    
class Region(GenericAPIView):

    @is_token_validate
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['token'])
            user = get_user_by_id_string(user_id_string)
            serializer = RegionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                region_obj = serializer.create(serializer.validated_data, user)
                view_serializer = RegionViewSerializer(instance=region_obj, context={'request': request})
                return Response({
                        STATE: SUCCESS,
                        RESULT: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                        STATE: ERROR,
                        RESULT: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

