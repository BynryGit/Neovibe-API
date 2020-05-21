import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.document import get_document_by_user_id
from v1.commonapp.models.document_type import get_document_type_by_name
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_master import get_user_by_id_string, get_user_by_id
from v1.userapp.serializers.document import DocumentViewSerializer, DocumentSerializer

# API Header
# API end Point: api/v1/user/:/note
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Get, Add, Edit user role and privilege
# Usage: Get, Add, Edit User role and privileges
# Tables used: 2.5.12 Notes
# Author: Arpita
# Created on: 14/05/2020
# Updated on: 21/05/2020


class UserDocument(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    data = []
                    user = get_user_by_id_string(id_string)
                    document_type = get_document_type_by_name('User')
                    user_document_obj = get_document_by_user_id(user.id,document_type.id)
                    if user_document_obj:
                        for user_document in user_document_obj:
                            serializer = DocumentViewSerializer(instance=user_document, context={'request': request})
                            data.append(serializer.data)
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: data,
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
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    user = get_user_by_id(3)
                    request.data['identification_id'] = str(id_string)
                    serializer = DocumentSerializer(data=request.data)
                    if serializer.is_valid():
                        document_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = DocumentViewSerializer(instance=document_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: view_serializer.data,
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
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
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    data = []
                    if is_user_role_data_verified(request):
                        user = get_user_by_id(3)
                        for role in request.data['roles']:
                            validate_data = {'user_id': str(id_string), 'role_id': role['role_id_string'],
                                             "is_active": role['is_active']}
                            serializer = UserRoleSerializer(data=validate_data)
                            if serializer.is_valid():
                                user_role = get_record_by_values(str(id_string), validate_data['role_id'])
                                if user_role:
                                    user_role_obj = serializer.update(user_role, serializer.validated_data, user)
                                else:
                                    user_role_obj = serializer.create(serializer.validated_data, user)
                                view_serializer = UserRoleViewSerializer(instance=user_role_obj,
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
