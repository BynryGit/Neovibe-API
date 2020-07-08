import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from master.models import get_all_users, get_user_by_id_string, is_email_exists
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.userapp.serializers.user import UserListSerializer, UserViewSerializer, UserSerializer


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
# Updated on: 21/05/2020


class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('first_name', 'last_name', 'tenant__id_string')
    ordering_fields = ('first_name', 'last_name',)
    ordering = ('created_date',)  # always give by default alphabetical order
    search_fields = ('first_name', 'email',)

    # @is_token_validate
    # @role_required(ADMIN, USER, VIEW)
    def get_queryset(self):
        queryset = get_all_users()
        return queryset


# API Header
# API end Point: api/v1/user
# API verb: POST
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Add users
# Usage: Add User
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 13/05/2020
# Updated on: 14/05/2020

class User(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                if not is_email_exists(request.data['email']):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    user_obj = serializer.create(serializer.validated_data, user)
                    view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_201_CREATED)
                else:
                    raise CustomAPIException("User already exists.", status_code=status.HTTP_409_CONFLICT)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/user/:id_string
# API verb: GET, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View users, Edit users
# Usage: View, Edit User
# Tables used: 2.5.3. Users & Privileges - User Details
# Author: Arpita
# Created on: 13/05/2020
# Updated on: 21/05/2020


class UserDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            if user:
                serializer = UserViewSerializer(instance=user, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    user_obj = serializer.update(user_obj, serializer.validated_data, user)
                    view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
