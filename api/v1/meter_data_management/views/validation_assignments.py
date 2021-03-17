__author__ = "chinmay"


from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.serializers.validation_assignments import ValidationAssignmentListSerializer, ValidationAssignmentViewSerializer, ValidationAssignmentSerializer
from v1.meter_data_management.models.validation_assignments import \
    ValidationAssignment as ValidationAssignmentModel,get_validation_assignment_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string

from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/meter-data/:id_string/validation-assignment/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Validation Assignment list
# Usage: API will fetch all Validation Assignment list
# Tables used: Validation Assignment
# Author: Chinmay
# Created on: 27/2/2021


class ValidationAssignmentList(generics.ListAPIView):
    try:
        serializer_class = ValidationAssignmentListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ValidationAssignmentModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Assignment not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/meter-data/validation-assignment
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Validation Assignment post
# Usage: API will Post the Validation Assignment
# Tables used: ValidationAssignment
# Author: Chinmay
# Created on: 27/2/2021
class ValidationAssignment(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ValidationAssignmentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                validation_assignment_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ValidationAssignmentViewSerializer(instance=validation_assignment_obj, context={'request': request})
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
# API end Point: api/v1/meter-data/validation-assignment/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Validation Assignment corresponding to the id
# Usage: API will fetch and update Validation Assignments for a given id
# Tables used: ValidationAssignment
# Author: Chinmay
# Created on: 27/2/2020


class ValidationAssignmentDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            validation_assignment = get_validation_assignment_by_id_string(id_string)
            if validation_assignment:
                serializer = ValidationAssignmentSerializer(instance=validation_assignment, context={'request': request})
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
            validation_assignment_obj = get_validation_assignment_by_id_string(id_string)
            if validation_assignment_obj:
                serializer = ValidationAssignmentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    validation_assignment_obj = serializer.update(validation_assignment_obj, serializer.validated_data, user)
                    view_serializer = ValidationAssignmentViewSerializer(instance=validation_assignment_obj,
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