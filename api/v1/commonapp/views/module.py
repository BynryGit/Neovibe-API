import traceback
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from v1.commonapp.models.module import get_all_modules, get_module_by_id_string
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination

# API Header
# API end Point: api/v1/module/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Sub Modules
# Usage: This will get the list of sub modules
# Tables used: 2.12.26 Lookup - Module, 2.12.3. Lookup - Sub Module
# Author: Priyanka
# Created on: 02/10/2020
# Updated on: 12/05/2020


class ModuleList(generics.ListAPIView):
    serializer_class = ModuleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = get_all_modules()
        utility_id_string = self.request.query_params.get('utility', None)
        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        return queryset


# API Header
# API end Point: api/v1/submodule
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Sub Module
# Usage: This will get the detail of sub modules
# Tables used: 2.12.26 Lookup - Module, 2.12.3. Lookup - Sub Module
# Author: Arpita
# Created on: 12/05/2020


class Module(GenericAPIView):

    def get(self, request, id_string):
        try:
            module = get_module_by_id_string(id_string)
            if module:
                serializer = ModuleViewSerializer(instance=module, context={'request': request})
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


