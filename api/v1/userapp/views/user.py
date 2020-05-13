import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_master import get_users_by_tenant_id_string, get_user_by_id_string
from v1.userapp.models.user_role import get_role_by_id_string
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_type import get_user_type_by_id_string
from v1.userapp.serializers.user import UserListSerializer, UserViewSerializer


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
# Created on: 12/05/2020

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
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic role details start
                        user = get_user_by_id_string(request.data['user'])
                        role, result, error = add_basic_role_details(request, user)
                        if result:
                            data = {
                                "role_id_string": role.id_string
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
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        user = get_user_by_id_string(request.data['user'])
                        role, result, error = save_edited_basic_role_details(request, user)
                        if result:
                            data = {
                                "role_id_string": role.id_string
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
                        # Save basic details start
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,

                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

