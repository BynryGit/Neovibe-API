__author__ = "aki"

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT, METER_READING_NOT_FOUND
from master.models import get_user_by_id_string
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.meter_reading import get_meter_reading_by_id_string
from v1.meter_data_management.serializers.meter_reading_validation_one import MeterReadingValidationOneSerializer
from v1.userapp.decorators import is_token_validate
from v1.commonapp.common_functions import get_user_from_token


# API Header
# API end Point: api/v1/meter-data/validation-one
# API verb: POST
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Update meter reading object and route task Assignment obj
# Usage: API will Update meter reading object and route task Assignment obj based on valid data
# Tables used: Meter Reading, Route Task Assignment
# Author: Akshay
# Created on: 18/03/2021

class MeterReadingValidationOneDetail(GenericAPIView):
    @is_token_validate
    #role_required(MX, METER_DATA, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            meter_reading_obj = get_meter_reading_by_id_string(id_string)
            if meter_reading_obj:
                meter_reading_serializer = MeterReadingValidationOneSerializer(data=request.data)
                if meter_reading_serializer.is_valid():
                    meter_reading_obj = meter_reading_serializer.update(meter_reading_obj,
                                                                        meter_reading_serializer.validated_data, user)
                    return Response({
                        STATE: SUCCESS,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: meter_reading_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: METER_READING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
