from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.meter_reading.serializers.schedule import ScheduleSerializer, ScheduleViewSerializer
from v1.userapp.models.user_master import UserDetail


# API Header
# API end Point: api/v1/meter-data/schedule
# API verb: POST
# Package: Basic
# Modules: Consumer Ops
# Sub Module: Meter data/schedule
# Interaction: Add schedule
# Usage: Add
# Tables used: Schedule
# Auther: Rohan
# Created on: 02/06/2020
class Schedule(GenericAPIView):

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    user = UserDetail.objects.get(id=2)
                    serializer = ScheduleSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=False):
                        schedule_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = ScheduleViewSerializer(instance=schedule_obj,
                                                                     context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULT: view_serializer.data,
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULT: list(serializer.errors.values())[0][0],
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: UNAUTHORIZED,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: UNAUTHORIZED,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)