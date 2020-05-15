__author__ = "aki"

import traceback
from rest_framework.response import Response
from rest_framework import generics, status
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.serializers.status import StatusSerializer
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.utility.models.utility_status import UtilityStatus


# API Header
# API end Point: api/v1/status
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: city list
# Usage: API will fetch all city list
# Tables used: UtilityStatus
# Author: Akshay
# Created on: 15/05/2020


class StatusList(generics.ListAPIView):

    def get(self, request):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    status_obj = UtilityStatus.objects.filter(is_active=True)
                    if status_obj:
                        serializer = StatusSerializer(status_obj, many=True)
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: serializer.data,
                        }, status=status.HTTP_200_OK)
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