__author__ = "aki"

import traceback
from rest_framework import generics
from v1.commonapp.serializers.country import CountrySerializer
from v1.tenant.models.tenant_country import TenantCountry as TenantCountryTbl
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger

# API Header
# API end Point: api/v1/countries
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: country list
# Usage: API will fetch all country list
# Tables used: Country
# Author: Akshay
# Created on: 15/05/2020


class CountryList(generics.ListAPIView):

    def get(self, request):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['Authorization']):
                response, user_obj = is_token_valid(self.request.headers['Authorization'])
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized(1,1,1,user_obj):
                # Checking authorization end

                    country_obj = TenantCountryTbl.objects.filter(is_active=True)
                    if country_obj:
                        serializer = CountrySerializer(country_obj, many=True)
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