import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_utility import get_utility_by_user, get_record_by_values
from v1.userapp.serializers.user_utility import UserUtilitySerializer, UserUtilityViewSerializer
from v1.userapp.views.common_functions import is_user_utility_data_verified, set_user_utility_validated_data
from v1.utility.models.utility_master import get_utility_by_id
from v1.utility.serializers.utility import UtilityMasterViewSerializer


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

    def get(self, request, id_string):
        try:
            response, user_obj = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility_list = []
                    user = get_user_by_id_string(id_string)
                    user_utilities = get_utility_by_user(user.id)
                    if user_utilities:
                        for user_utility in user_utilities:
                            utility_obj = get_utility_by_id(user_utility.utility_id)
                            utility = UtilityMasterViewSerializer(instance=utility_obj, context={'request': request})
                            utility_list.append(utility.data)
                        return Response({
                            STATE: SUCCESS,
                            DATA: utility_list,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: ERROR,
                            DATA: 'No records found.',
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id_string):
        try:
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    if is_user_utility_data_verified(request):
                        for utility in request.data['utilities']:
                            validate_data = {'user_id': str(id_string), 'utility_id': utility['utility_id_string']}
                            serializer = UserUtilitySerializer(data=validate_data)
                            if serializer.is_valid(raise_exception=False):
                                user_utility_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = UserUtilityViewSerializer(instance=user_utility_obj,
                                                                         context={'request': request})
                                data.append(view_serializer.data)
                            else:
                                return Response({
                                    STATE: ERROR,
                                    RESULTS: serializer.errors,
                                }, status=status.HTTP_400_BAD_REQUEST)
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: data,
                        }, status=status.HTTP_201_CREATED)
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
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    def put(self, request, id_string):
        try:
            response, user = is_token_valid(self.request.headers['token'])
            if response:
                if is_authorized(1, 1, 1, user):
                    data = []
                    if is_user_utility_data_verified(request):
                        for utility in request.data['utilities']:
                            validate_data = {'user_id': str(id_string), 'utility_id': utility['utility_id_string'],
                                             "is_active": utility['is_active']}
                            validated_data = set_user_utility_validated_data(validate_data)
                            serializer = UserUtilitySerializer(data=validated_data)
                            if serializer.is_valid(raise_exception=False):
                                user_utility = get_record_by_values(str(id_string), validate_data['utility_id'])
                                if user_utility:
                                    user_utility_obj = serializer.update(user_utility, serializer.validated_data, user)
                                else:
                                    user_utility_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = UserUtilityViewSerializer(instance=user_utility_obj,
                                                                         context={'request': request})
                                data.append(view_serializer.data)
                            else:
                                return Response({
                                    STATE: ERROR,
                                    RESULTS: serializer.errors,
                                }, status=status.HTTP_400_BAD_REQUEST)
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: data,
                        }, status=status.HTTP_200_OK)
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
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)