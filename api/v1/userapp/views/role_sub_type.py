__author__ = "priyanka"

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from api.constants import ADMIN, VIEW, TENANT, EDIT
from v1.userapp.models.role_type import get_role_type_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULT
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from master.models import get_user_by_id_string
from v1.userapp.models.role_sub_type import RoleSubType as RoleSubTypeTbl
from v1.userapp.serializers.role_sub_type import GetRoleSubTypeSerializer



# API Header
# API end Point: api/v1/role-type/id_string/role-subtype/list
# API verb: GET
# Package: Basic
# Modules: Userapp
# Sub Module: Role
# Interaction: Role subtype list by roletype is_string
# Usage: API will fetch Role subtype list against single roletype
# Tables used: RoleSubType
# Author: priyanka
# Created on: 20/10/2020


class RoleSubTypeByRoleType(generics.ListAPIView):
    try:
        serializer_class = GetRoleSubTypeSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant__id_string',)
        ordering = ('tenant__name',)  # always give by default alphabetical order
        search_fields = ('tenant__name',)

        def get_queryset(self):
            token, user_obj = is_token_valid(self.request.headers['Authorization'])
            if token:
                if is_authorized(1,1,1,user_obj):
                    role_type_obj = get_role_type_by_id_string(self.kwargs['id_string'])
                    if role_type_obj:
                        queryset = RoleSubTypeTbl.objects.filter(role_type_id=role_type_obj.id, is_active=True)
                        return queryset
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='TENANT/SUBMODULE')
        raise APIException

