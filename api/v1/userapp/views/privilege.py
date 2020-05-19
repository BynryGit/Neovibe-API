import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.privilege import get_all_privilege
from v1.userapp.serializers.privilege import PrivilegeListSerializer


# API Header
# API end Point: api/v1/user/privilege/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View privilege list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Privilege
# Author: Arpita
# Created on: 19/05/2020


class PrivilegeList(generics.ListAPIView):
    serializer_class = PrivilegeListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('tenant__id_string', 'utility__id_string')
    ordering_fields = ('name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('name',)

    def get_queryset(self):
        queryset = get_all_privilege()
        return queryset
