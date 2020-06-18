import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.models.document import get_document_by_user_id, get_document_by_id_string
from v1.commonapp.models.document_type import get_document_type_by_name
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required, utility_required
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

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
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
                    RESULTS: '',
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @utility_required
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, id_string):
        try:
            request.data['identification_id'] = str(id_string)
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                user_id_string = get_user_from_token(request.headers['token'])
                user = get_user_by_id_string(user_id_string)
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
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @utility_required
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            request.data['identification_id'] = str(id_string)
            document = get_document_by_id_string(request.data['document_id'])
            if document:
                serializer = DocumentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    document_obj = serializer.update(document, serializer.validated_data, user)
                    view_serializer = DocumentViewSerializer(instance=document_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)
