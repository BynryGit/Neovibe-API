__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_services_number_format import \
    UtilityServiceNumberFormat as UtilityServiceNumberFormatTbl, \
    get_utility_service_number_format_by_utility_id_string_and_item
from v1.utility.serializers.numformat import UtilityServiceNumberFormatSerializer


# API Header
# API end Point: api/v1/utility/id_string/numformat
# API verb: PUT
# Package: Basic
# Modules: Utility
# Sub Module: Numformat
# Interaction: for edit numformat
# Usage: API will edit numformat and return updated current number
# Tables used: 2.5.12 Notes
# Author: Akshay
# Created on: 14/05/2020


class UtilityNumformatDetail(GenericAPIView):
    serializer_class = UtilityServiceNumberFormatTbl

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

                    numformat_obj = get_utility_service_number_format_by_utility_id_string_and_item(id_string, request.data['item'])

                    if numformat_obj:
                        serializer = UtilityServiceNumberFormatSerializer(data=request.data)
                        if serializer.is_valid():
                            numformat_obj = serializer.update(numformat_obj, serializer.validated_data, user)
                            if numformat_obj.prefix:
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: {'numformat_obj': str(numformat_obj.prefix) + str(numformat_obj.currentno)},
                                }, status=status.HTTP_200_OK)
                            else:
                                return Response({
                                    STATE: SUCCESS,
                                    RESULT: {'numformat_obj': numformat_obj.currentno},
                                }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: SUCCESS,
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