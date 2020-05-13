__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.utility.models.utility_module import get_utility_module_by_id_string
from v1.utility.models.utility_sub_module import UtilitySubModule
from v1.utility.serializers.utility_sub_module import UtilitySubModuleViewSerializer


# API Header
# API end Point: api/v1/utilities/id_string/submodule
# API verb: GET
# Package: Basic
# Modules: Utility
# Sub Module: SubModule
# Interaction: Utility Submodule list
# Usage: API will fetch required data for utility Submodule list against single utility module
# Tables used: 2.4 Utility SubModule
# Author: aki
# Created on: 12/05/2020


class UtilitySubModuleDetail(GenericAPIView):

    def get(self, request, utility, module):
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

                    utility_module_obj = get_utility_module_by_id_string(module)
                    if utility_module_obj:
                        utility_submodule_obj = UtilitySubModule.objects.filter(module_id=utility_module_obj.id, utility__id_string=utility, is_active=True)
                        if utility_submodule_obj:
                            serializer = UtilitySubModuleViewSerializer(utility_submodule_obj, many=True, context={'request': request})
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