import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl
from v1.utility.serializers.utility import UtilityMasterViewSerializer, UtilityMasterSerializer
from rest_framework.response import Response


# API Header
# API end Point: api/v1/utility
# API verb: GET
# Package: Basic
# Modules:
# Sub Module:
# Interaction: Utility list
# Usage: API will fetch required data for utility list against filter and search
# Tables used: 2.1. Utility Master
# Author: aki
# Created on: 08/05/2020

class UtilityListDetail(generics.ListAPIView):
    serializer_class = UtilityMasterViewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_str = self.request.query_params.get('search', None)
        filter_str = self.request.query_params.get('filter', None)
        print(search_str, filter_str)

        if not filter_str:
            filter_str = 'ALL'

        if search_str and filter_str != 'ALL':
            queryset = UtilityMasterTbl.objects.filter(is_deleted=False, name__icontains=search_str,
                                                 tenant_id=filter_str).order_by('-id')
        elif search_str and filter_str == 'ALL':
            queryset = UtilityMasterTbl.objects.filter(is_deleted=False, name__icontains=search_str).order_by('-id')

        elif not search_str and filter_str != 'ALL':
            queryset = UtilityMasterTbl.objects.filter(is_deleted=False, tenant_id=filter_str).order_by('-id')
        else:
            queryset = UtilityMasterTbl.objects.filter(is_deleted=False).order_by('-id')

        return queryset


# API Header
# API end Point: api/v1/utility
# API verb: GET
# Package: Basic
# Modules:
# Sub Module:
# Interaction: Utility fot get and edit
# Usage: API will fetch required data for utility list against single utility id_string and edit the existing utility
# Tables used: 2.1. Utility Master
# Author: aki
# Created on: 08/05/2020

class UtilityDetail(GenericAPIView):
    serializer_class = UtilityMasterSerializer

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

                    utility_obj = UtilityMasterTbl.objects.filter(id_string=id_string)
                    if utility_obj:
                        utility_obj = UtilityMasterTbl.objects.get(id_string=id_string)
                        serializer = UtilityMasterViewSerializer(instance=utility_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)