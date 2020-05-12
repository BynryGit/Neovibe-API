import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from api import messages
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_master import get_users_by_tenant_id_string
from v1.userapp.serializers.user import UserListSerializer
from v1.userapp.views.common_functions import login, authentication


# API Header
# API end Point: api/v1/user/login
# API verb: GET
# Package: Basic
# Modules: User
# Interaction: user list
# Usage: API will fetch required data for user list
# Tables used: 2.5.3. User Details
# Author: Arpita
# Created on: 29/04/2020


class LoginApiView(APIView):
    """Login Api View"""
    def post(self, request, format=None):
        try:
            validated_data = {
                'username': request.data['username'],
                'password': request.data['password']
            }

            auth = authentication(validated_data)

            if auth:
                token = login(auth) # Call Login function

                if not token:
                    return Response({
                        messages.RESULT: messages.FAIL,
                        messages.MESSAGE: messages.INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        messages.RESULT: messages.SUCCESS,
                        messages.MESSAGE: messages.SUCCESSFULLY_DATA_RETRIEVE,
                        messages.Token: token,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    messages.RESULT: messages.FAIL,
                    messages.MESSAGE: messages.INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        utility_id_string = self.requestUserRole.objects.filter(tenant_id=1).query_params.get('utility', None)
        type_id_string = self.request.query_params.get('type', None)
        sub_type_id_string = self.request.query_params.get('sub_type', None)
        form_factor_id_string = self.request.query_params.get('form_factor', None)
        department_id_string = self.request.query_params.get('department', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        if type_id_string is not None:
            role_type = get_role_type_by_id_string(type_id_string)
            queryset = queryset.filter(type_id=role_type.id)
        if sub_type_id_string is not None:
            role_sub_type = get_role_sub_type_by_id_string(sub_type_id_string)
            queryset = queryset.filter(sub_type_id=role_sub_type.id)
        if form_factor_id_string is not None:
            form_factor = get_form_factor_by_id_string(form_factor_id_string)
            queryset = queryset.filter(form_factor_id=form_factor.id)
        if department_id_string is not None:
            department = get_department_by_id_string(department_id_string)
            queryset = queryset.filter(department_id=department.id)
        return queryset
