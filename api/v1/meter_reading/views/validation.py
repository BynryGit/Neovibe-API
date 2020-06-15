__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from master.models import User
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.meter_reading.models.meter_reading import get_meter_reading_by_id_string
from v1.meter_reading.serializers.meter_reading import MeterReadingViewSerializer, MeterReadingSerializer

# API Header
# API end Point: api/v1/meterreading/id_string/validation
# API verb: PUT
# Package: Basic
# Modules: Meter Data
# Sub Module: Validation
# Interaction: For edit single validation
# Usage: API will edit and get validation
# Tables used: 2.3.8.4 Meter Reading
# Author: Akshay
# Created on: 15/06/2020


class ValidationDetail(GenericAPIView):
    serializer_class = MeterReadingSerializer

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # Todo fetch user from request start
                    user = User.objects.get(id=2)
                    # Todo fetch user from request end

                    validation_obj = get_meter_reading_by_id_string(id_string)
                    if validation_obj:
                        serializer = MeterReadingSerializer(data=request.data)
                        if serializer.is_valid():
                            validation_obj = serializer.update(validation_obj, serializer.validated_data, user)
                            serializer = MeterReadingViewSerializer(validation_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULT: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULT: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)