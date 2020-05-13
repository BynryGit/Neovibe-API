import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.serializers.role_type import RoleTypeListSerializer, RoleTypeViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.role_type import get_role_type_by_tenant_id_string, get_role_type_by_id_string


# API Header
# API end Point: api/v1/role_type/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Role Type
# Usage: This will get the list of role types
# Tables used: Lookup - Role Type
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020


class RoleTypeList(generics.ListAPIView):
    serializer_class = RoleTypeListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = get_role_type_by_tenant_id_string(1)
        utility_id_string = self.request.query_params.get('utility', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        return queryset


# API Header
# API end Point: api/v1/role_type
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Role Type
# Usage: This will get the detail of role types
# Tables used: Lookup - Role Type
# Author: Arpita
# Created on: 12/05/2020


class RoleType(GenericAPIView):

    def get(self, request, id_string):
        try:
            role_type = get_role_type_by_id_string(id_string)
            if role_type:
                serializer = RoleTypeViewSerializer(instance=role_type, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)