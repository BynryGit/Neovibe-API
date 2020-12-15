import traceback
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from v1.commonapp.models.sub_module import get_all_sub_modules, get_sub_module_by_id_string
from v1.commonapp.serializers.sub_module import SubModuleListSerializer, SubModuleViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination

# API Header
# API end Point: api/v1/submodule/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View Sub Modules
# Usage: This will get the list of sub modules
# Tables used: 2.12.26 Lookup - Module, 2.12.3. Lookup - Sub Module
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020


class SubModuleList(generics.ListAPIView):
    serializer_class = SubModuleListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = get_all_sub_modules()
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


class SubModule(GenericAPIView):

    def get(self, request, id_string):
        try:
            module = get_sub_module_by_id_string(id_string)
            if module:
                serializer = SubModuleViewSerializer(instance=module, context={'request': request})
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


# class SubModule(APIView):
#
#     def get(self, request, format=None):
#         try:
#             # Checking authentication start
#             if is_token_valid(request.data['token']):
#                 # payload = get_payload(request.data['token'])
#                 # user = get_user(payload['id_string'])
#                 # Checking authentication end
#
#                 # Checking authorization start
#                 # privilege = get_privilege_by_id(1)
#                 # sub_module = get_sub_module_by_id(1)
#                 if is_authorized():
#                     # Checking authorization end
#
#                     # Declare local variables start
#                     data_list = []
#                     sub_module_list = []
#                     # Declare local variables end
#
#                     # Code for lookups start
#                     modules = get_all_modules()
#                     # Code for lookups end
#
#                     # Code for sending departments in response start
#                     for module in modules:
#                         sub_modules = get_submodule_by_module_id(module.id)
#                         for sub_module in sub_modules:
#                             sub_module_list.append({
#                                 'sub_module_id_string': sub_module.id_string,
#                                 'sub_module_name': sub_module.id_string,
#                             })
#                         data = {'module_id_string': module.id_string, 'module_name': module.name,
#                                 'submodules': sub_module_list}
#                         data_list.append(data)
#                     return Response({
#                         STATE: SUCCESS,
#                         DATA: data_list,
#                     }, status=status.HTTP_200_OK)
#                     # Code for sending departments in response end
#
#                 else:
#                     return Response({
#                         STATE: ERROR,
#                         DATA: '',
#                     }, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                     DATA: '',
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({
#                 STATE: EXCEPTION,
#                 DATA: '',
#                 ERROR: str(traceback.print_exc(e))
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
