__author__ = "aki"

from rest_framework.exceptions import APIException
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.utility.serializers.utility_module_submodule import UtilityModuleSubmoduleViewSerializer


# API Header
# API end Point: api/v1/utility/id_string/module-submodule/list
# API verb: GET
# Package: Basic
# Modules: Utility
# Sub Module: Module
# Interaction: Get utility module and submodule list by utility id string
# Usage: API will fetch required data for utility module and submodule list against single utility
# Tables used: 2.3 Utility Module, 2.4 Utility SubModule
# Author: Akshay
# Created on: 02/11/2020


class UtilityModuleSubmoduleList(generics.ListAPIView):
    try:
        serializer_class = UtilityModuleSubmoduleViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string', 'utility__id_string')
        ordering_fields = ('tenant__name', 'utility__name')
        ordering = ('utility__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name', 'utility__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    queryset = UtilityModuleTbl.objects.filter(utility__id_string=self.kwargs['id_string'], is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/MODULE-SUBMODULE')
        raise APIException