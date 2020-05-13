__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.utility.models.utility_module import get_utility_modules_by_utility_id_string
from v1.utility.serializers.utility_module import UtilityModuleViewSerializer


# API Header
# API end Point: api/v1/utilities/id_string/module
# API verb: GET
# Package: Basic
# Modules: Utility
# Sub Module: Module
# Interaction: Utility module list
# Usage: API will fetch required data for utility module list against single utility
# Tables used: 2.3 Utility Module
# Author: aki
# Created on: 12/05/2020


class UtilityModuleDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end
                    # never pass token in logger
                    # choices = {'key1': 'val1', 'key2': 'val2'}
                    # logger.log("info", "Getting utility details", None, choices)

                    utility_module_obj = get_utility_modules_by_utility_id_string(id_string)
                    if utility_module_obj:
                        serializer = UtilityModuleViewSerializer(utility_module_obj, many=True, context={'request': request})
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
            # logger.log("Error", "Exception at GET api/v1/utilities/", ex )
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)