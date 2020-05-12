__author__ = "aki"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.utility.models.utility_usage_summary import get_utility_usage_summary_by_utility_id_string
from v1.utility.serializers.summary import UtilityUsageSummaryViewSerializer


# API Header
# API end Point: api/v1/utilities/id_string/summary
# API verb: GET
# Package: Basic
# Modules: Utility
# Sub Module: sammary
# Interaction: Utility summary
# Usage: API will fetch all summary against utility
# Tables used: 2.3  Utility Usage Summary
# Author: aki
# Created on: 12/05/2020


class UtilityUsageSummaryDetail(GenericAPIView):

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

                    utility_summary_obj = get_utility_usage_summary_by_utility_id_string(id_string)
                    if utility_summary_obj:
                        serializer = UtilityUsageSummaryViewSerializer(instance=utility_summary_obj, context={'request': request})
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