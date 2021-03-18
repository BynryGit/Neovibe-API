from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.serializers.utility_working_hours import WorkingHourViewSerializer, WorkingHourSerializer, WorkingHourListSerializer
from v1.utility.models.utility_working_hours import UtilityWorkingHours as UtilityWorkingHoursModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_working_hours import get_utility_working_hours_by_id_string
from api.messages import UTILITY_WORKING_HOURS_NOT_FOUND, SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from api.constants import *

# API Header
# API end Point: api/v1/utility/:id_string/working_hours/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Area list
# Usage: API will fetch all Working Hours list
# Tables used: Holiday Working Hours
# Author: Chinmay
# Created on: 11/1/2021


class WorkingHourList(generics.ListAPIView):
    try:
        serializer_class = WorkingHourListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityWorkingHoursModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(UTILITY_WORKING_HOURS_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/working_hours
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Utility Holiday post
# Usage: API will Post the holiday
# Tables used: Holiday Calendar
# Author: Chinmay
# Created on: 11/1/2020
class WorkingHour(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = WorkingHourSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                working_hour_obj = serializer.create(serializer.validated_data, user)
                view_serializer = WorkingHourViewSerializer(instance=working_hour_obj, context={'request': request})
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
# API end Point: api/v1/utility/working_hour/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Area corresponding to the id
# Usage: API will fetch and update Working Hours for a given id
# Tables used: Working Hours
# Author: Chinmay
# Created on: 10/11/2020


class WorkingHourDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            working_hour = get_utility_working_hours_by_id_string (id_string)
            if working_hour:
                serializer = WorkingHourViewSerializer(instance=working_hour, context={'request': request})
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
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            working_hour_obj = get_utility_working_hours_by_id_string(id_string)
            if working_hour_obj:
                serializer = WorkingHourSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    working_hour_obj = serializer.update(working_hour_obj, serializer.validated_data, user)
                    view_serializer = WorkingHourViewSerializer(instance=working_hour_obj,
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
