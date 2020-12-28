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
from v1.userapp.models.user_area import get_area_by_user_id, get_record_by_values
from v1.userapp.serializers.user_area import UserAreaSerializer, UserAreaViewSerializer
from v1.userapp.views.common_functions import set_user_area_validated_data


# API Header
# API end Point: api/v1/user/:id_string/area
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit user area
# Usage: View, Add, Edit User Area
# Tables used: 2.5 Users & Privileges - User Area
# Author: Arpita
# Created on: 02/06/2020


class UserArea(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            area_list = []
            data = {}
            user = get_user_by_id_string(id_string)
            if user:
                data['email'] = user.email
                data['id_string'] = id_string
                user_areas = get_area_by_user_id(user.id)
                if user_areas:
                    for user_area in user_areas:
                        area = UserAreaViewSerializer(instance=user_area, context={'request': request})
                        area_list.append(area.data['area'])
                    data['areas'] = area_list
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: AREA_NOT_ASSIGNED,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Area')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request, id_string):
        try:
            data = {}
            area_list = []
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for area in request.data:
                    # validate_data = {'user_id': str(id_string), 'utility_id': request.data['utility_id'], 'area_id': area['area_id_string']}
                    validate_data = {'user_id': str(id_string),'area_id': area['area_id_string']}
                    serializer = UserAreaSerializer(data=validate_data)
                    if serializer.is_valid(raise_exception=False):
                        user_id_string = get_user_from_token(request.headers['Authorization'])
                        user = get_user_by_id_string(user_id_string)
                        user_area_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserAreaViewSerializer(instance=user_area_obj, context={'request': request})
                        area_list.append(view_serializer.data['area'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['areas'] = area_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                 }, status=status.HTTP_201_CREATED)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Area')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER,  EDIT)
    def put(self, request, id_string):
        try:
            data = {}
            area_list = []
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for area in request.data['areas']:
                    validate_data = {'user_id': str(id_string), 'area_id': area['area_id_string'],
                                     "is_active": area['is_active']}
                    validated_data = set_user_area_validated_data(validate_data)
                    serializer = UserAreaSerializer(data=validated_data)
                    if serializer.is_valid(raise_exception=False):
                        user_area = get_record_by_values(str(id_string), validate_data['area_id'])
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        if user_area:
                            user_area_obj = serializer.update(user_area, serializer.validated_data, user)
                        else:
                            user_area_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserAreaViewSerializer(instance=user_area_obj,
                                                                 context={'request': request})
                        area_list.append(view_serializer.data['area'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['areas'] = area_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_200_OK)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Area')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

