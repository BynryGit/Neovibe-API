from rest_framework import status, generics
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_master import get_users_by_tenant_id_string
from v1.userapp.models.user_role import get_role_by_id_string
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_type import get_user_type_by_id_string
from v1.userapp.serializers.user import UserListSerializer

# API Header
# API end Point: api/v1/role/list
# API verb: GET
# Package: Basic
# Modules: Roles & Privileges
# Sub Module: Role
# Interaction: View role list
# Usage: Used for role list. Gets all the records in pagination mode. It also have input params to filter/search and
# sort in addition to pagination.
# Tables used: 2.5.1. Users & Privileges - Role Master
# Author: Arpita
# Created on: 11/05/2020


class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        queryset = get_users_by_tenant_id_string(1)
        utility_id_string = self.request.query_params.get('utility', None)
        city_id_string = self.request.query_params.get('city', None)
        user_type_id_string = self.request.query_params.get('user_type', None)
        user_sub_type_id_string = self.request.query_params.get('user_sub_type', None)
        form_factor_id_string = self.request.query_params.get('form_factor', None)
        department_id_string = self.request.query_params.get('department', None)
        role_id_string = self.request.query_params.get('role', None)
        status_id_string = self.request.query_params.get('status', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        if city_id_string is not None:
            city = get_city_by_id_string(city_id_string)
            queryset = queryset.filter(city_id=city.id)
        if user_type_id_string is not None:
            user_type = get_user_type_by_id_string(user_type_id_string)
            queryset = queryset.filter(user_type_id=user_type.id)
        if user_sub_type_id_string is not None:
            user_sub_type = get_user_sub_type_by_id_string(user_sub_type_id_string)
            queryset = queryset.filter(user_subtype_id=user_sub_type.id)
        if form_factor_id_string is not None:
            form_factor = get_form_factor_by_id_string(form_factor_id_string)
            queryset = queryset.filter(form_factor_id=form_factor.id)
        if department_id_string is not None:
            department = get_department_by_id_string(department_id_string)
            queryset = queryset.filter(department_id=department.id)
        if role_id_string is not None:
            role = get_role_by_id_string(role_id_string)
            queryset = queryset.filter(role_id=role.id)
        if status_id_string is not None:
            status = get_user_status_by_id_string(status_id_string)
            queryset = queryset.filter(status_id=status.id)
        return queryset
