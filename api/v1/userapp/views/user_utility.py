import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.userapp.models.user_utility import get_utility_by_user, get_record_by_values
from v1.userapp.serializers.user_utility import UserUtilitySerializer, UserUtilityViewSerializer
from v1.userapp.views.common_functions import set_user_utility_validated_data


# API Header
# API end Point: api/v1/user/:id_string/data-access
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit user data access
# Usage: View, Add, Edit User data access
# Tables used: 2.5 Users & Privileges - User Utility
# Author: Arpita
# Created on: 02/06/2020


class UserUtility(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            utility_list = []
            data = {}
            user = get_user_by_id_string(id_string)
            if user:
                data['email'] = user.email
                data['id_string'] = id_string
                user_utilities = get_utility_by_user(user.id)
                if user_utilities:
                    for user_utility in user_utilities:
                        utility = UserUtilityViewSerializer(instance=user_utility, context={'request': request})
                        utility_list.append(utility.data['utility'])
                    data['utilities'] = utility_list
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: UTILITY_NOT_ASSIGNED,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Utility')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, id_string):
        try:
            utility_list = []
            data = {}
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for utility in request.data['utilities']:
                    validate_data = {'user_id': str(id_string), 'utility_id': utility['utility_id_string']}
                    serializer = UserUtilitySerializer(data=validate_data)
                    if serializer.is_valid(raise_exception=False):
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        user_utility_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserUtilityViewSerializer(instance=user_utility_obj,
                                                                 context={'request': request})
                        utility_list.append(view_serializer.data['utility'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['utilities'] = utility_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_201_CREATED)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            utility_list = []
            data = {}
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for utility in request.data['utilities']:
                    validate_data = {'user_id': str(id_string), 'utility_id': utility['utility_id_string']}
                    validated_data = set_user_utility_validated_data(validate_data)
                    serializer = UserUtilitySerializer(data=validated_data)
                    if serializer.is_valid(raise_exception=False):
                        user_utility = get_record_by_values(str(id_string), validate_data['utility_id'])
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        if user_utility:
                            user_utility_obj = serializer.update(user_utility, serializer.validated_data, user)
                        else:
                            user_utility_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserUtilityViewSerializer(instance=user_utility_obj,
                                                                 context={'request': request})
                        utility_list.append(view_serializer.data['utility'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['utilities'] = utility_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_200_OK)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)