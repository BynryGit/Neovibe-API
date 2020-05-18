import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_master import get_users_by_tenant_id_string, get_user_by_id_string, get_all_users
from v1.userapp.models.role import get_role_by_id_string
from v1.userapp.models.user_privilege import get_user_privilege_by_user_id
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_type import get_user_type_by_id_string
from v1.userapp.serializers.user import UserListSerializer, UserViewSerializer, UserPrivilegeViewSerializer

# API Header
# API end Point: api/v1/user/list
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View user list
# Usage: Used for user list. Get all the records in pagination mode. It also have input params to filter/ search and
# sort in addition to pagination.
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 11/05/2020
from v1.userapp.views.common_functions import is_user_data_verified, add_basic_user_details, \
    save_edited_basic_user_details, is_privilege_data_verified, add_user_privilege, save_edited_privilege


class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('tenant__id_string', 'utility__id_string')
    # filter_fields = ('tenant__id_string', 'utility__id_string', 'city_id_string', 'user_type_id_string', 'user_sub_type_id_string', 'form_factor_id_string', 'department_id_string', 'role_id_string', 'status_id_string')
    ordering_fields = ('first_name', 'last_name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('first_name', 'email_id')

    def get_queryset(self):

        queryset = get_all_users()
        return queryset


# API Header
# API end Point: api/v1/user
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View users, Add users, Edit users
# Usage: View, Add, Edit User
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 13/05/2020
# Updated on: 14/05/2020

class Users(GenericAPIView):

    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            if user:
                serializer = UserViewSerializer(instance=user, context={'request': request})
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

    def post(self, request, format=None):
        try:

            # Request data verification start
            if is_user_data_verified(request):
                # Request data verification end

                # Save basic user details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = add_basic_user_details(request, user)
                if result:
                    data = {
                        "user_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Save basic role details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:

            # Request data verification start
            if is_user_data_verified(request):
                # Request data verification end

                # Edit basic details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = save_edited_basic_user_details(request, user)
                if result:
                    data = {
                        "user_detail_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Edit basic details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/user/role
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Get user role list
# Usage: get User role and privileges
# Tables used: 2.5.2. Users & Privileges - Role Privileges
# Author: Arpita
# Created on: 14/05/2020


class UserPrivilege(GenericAPIView):

    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            privileges = get_user_privilege_by_user_id(user.id)
            for privilege in privileges:
                serializer = UserPrivilegeViewSerializer(instance=privilege, context={'request': request})

            if user:
                serializer = UserPrivilegeViewSerializer(instance=user, context={'request': request})
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


# API Header
# API end Point: api/v1/user/role
# API verb: POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Add user notes, Edit user role and privilege
# Usage: Add, Edit User role and privileges
# Tables used: 2.5.2. Users & Privileges - Role Privileges
# Author: Arpita
# Created on: 14/05/2020

class UserRole(GenericAPIView):

    def post(self, request, format=None):
        try:

            # Request data verification start
            if is_privilege_data_verified(request):
                # Request data verification end

                # Save basic user details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = add_user_privilege(request, user)
                if result:
                    data = {
                        "user_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Save basic role details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:

            # Request data verification start
            if is_privilege_data_verified(request):
                # Request data verification end

                # Edit basic details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = save_edited_privilege(request, user)
                if result:
                    data = {
                        "user_detail_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Edit basic details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
