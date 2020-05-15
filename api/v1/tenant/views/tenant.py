import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import TenantMaster as TenantMasterTbl
# from v1.tenant.serializers.tenant import TenantMasterViewSerializer, TenantMasterSerializer
from rest_framework.response import Response


# API Header
# API end Point: api/v1/tenant/list
# API verb: GET
# Package: Basic
# Modules:
# Sub Module:
# Interaction: Utility list
# Usage: API will fetch required data for utility list against filter and search
# Tables used: 1.1. Tenant Master
# Author: Gauri
# Created on: 13/05/2020

class TenantListDetail(generics.ListAPIView):
    # serializer_class = TenantMasterViewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_str = self.request.query_params.get('search', None)
        filter_str = self.request.query_params.get('filter', None)
        print(search_str, filter_str)

        if not filter_str:
            filter_str = 'ALL'

        if search_str and filter_str != 'ALL':
            queryset = TenantMasterTbl.objects.filter(is_active=True, name__icontains=search_str,
                                                 tenant_id=filter_str).order_by('-id')
        elif search_str and filter_str == 'ALL':
            queryset = TenantMasterTbl.objects.filter(is_active=True, name__icontains=search_str).order_by('-id')

        elif not search_str and filter_str != 'ALL':
            queryset = TenantMasterTbl.objects.filter(is_active=True, tenant_id=filter_str).order_by('-id')
        else:
            queryset = TenantMasterTbl.objects.filter(is_active=True).order_by('-id')

        return queryset


# API Header
# API end Point: api/v1/tenant
# API verb: GET
# Package: Basic
# Modules:
# Sub Module:
# Interaction: Tenant fot get and edit
# Usage: API will fetch required data for utility list against single utility id_string and edit the existing utility
# Tables used: 1.1. Utility Master
# Author: Gauri
# Created on: 13/05/2020

class TenantDetail(GenericAPIView):
    # serializer_class = TenantMasterSerializer

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

                    tenant_obj = TenantMasterTbl.objects.filter(id_string=id_string, is_active=True)
                    if tenant_obj:
                        # serializer = TenantMasterViewSerializer(instance=tenant_obj, context={'request': request})
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