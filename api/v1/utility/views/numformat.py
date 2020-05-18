__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat
from v1.utility.serializers.numformat import NumformatSerializer


# API Header
# API end Point: api/v1/utility/id_string/numformat
# API verb: PUT
# Package: Basic
# Modules: Utility
# Sub Module: Numformat
# Interaction: for edit numformat
# Usage: API will edit numformat and return updated current number
# Tables used: 2.5.12 Notes
# Author: Gauri Deshmukh
# Created on: 14/05/2020


class UtilityNumformatDetail(GenericAPIView):

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

                    numformat_obj = UtilityServiceNumberFormat.objects.filter(utility__id_string=id_string,
                                                                                 item=request.data['item'], is_active=True)
                    if numformat_obj:
                        serializer = NumformatSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.update(numformat_obj, serializer.validated_data, request.user)
                            return Response({
                                STATE: SUCCESS,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.errors,
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