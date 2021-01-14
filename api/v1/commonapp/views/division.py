__author__ = "aki"


from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
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
from v1.consumer.serializers.consumer_master import ConsumerSerializer, ConsumerViewSerializer
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.service.models.consumer_services import get_consumer_services_by_consumer_no
from v1.service.serializers.service import ServiceDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.serializers.division import DivisionSerializer, DivisionViewSerializer, DivisionListSerializer
from v1.commonapp.models.division import Division as DivisionModel
from v1.utility.models.utility_region import get_utility_region_by_id
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.division import get_division_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/utility/:id_string/division/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Division list
# Usage: API will fetch all Division list
# Tables used: Division
# Author: Chinmay
# Created on: 8/1/2021


class DivisionList(generics.ListAPIView):
    try:
        serializer_class = DivisionListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = DivisionModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Division not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/division
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Division post
# Usage: API will Post the Division
# Tables used: Division
# Author: Chinmay
# Created on: 8/1/2021
class Division(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = DivisionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                division_obj = serializer.create(serializer.validated_data, user)
                view_serializer = DivisionViewSerializer(instance=division_obj, context={'request': request})
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


# API Header
# API end Point: api/v1/utility/division/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Division corresponding to the id
# Usage: API will fetch and update Divisions for a given id
# Tables used: Division
# Author: Chinmay
# Created on: 8/1/2021


class DivisionDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            division = get_division_by_id_string(id_string)
            if division:
                serializer = DivisionViewSerializer(instance=division, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            division_obj = get_division_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = division_obj.name
            if division_obj:
                serializer = DivisionSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    division_obj = serializer.update(division_obj, serializer.validated_data, user)
                    view_serializer = DivisionViewSerializer(instance=division_obj,
                                                             context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)