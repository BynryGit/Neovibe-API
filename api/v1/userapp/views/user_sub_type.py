__author__ = "priyanka"

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
# #from api.constants import ADMIN, VIEW, TENANT, EDIT
from v1.userapp.models.user_type import get_user_type_by_id_string
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
from v1.userapp.models.user_sub_type import UserSubType as UserSubTypeTbl
from v1.userapp.serializers.user_sub_type import GetUserSubTypeSerializer



# API Header
# API end Point: api/v1/user-type/id_string/user-subtype/list
# API verb: GET
# Package: Basic
# Modules: Userapp
# Sub Module: User
# Interaction: User subtype list by Usertype is_string
# Usage: API will fetch User subtype list against single Usertype
# Tables used: UserSubType
# Author: priyanka
# Created on: 20/10/2020


class UserSubTypeByUserType(generics.ListAPIView):
    try:
        serializer_class = GetUserSubTypeSerializer
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
                    user_type_obj = get_user_type_by_id_string(self.kwargs['id_string'])
                    if user_type_obj:
                        queryset = UserSubTypeTbl.objects.filter(user_type_id=user_type_obj.id, is_active=True)
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

