import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string, User
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.models.notes import get_notes_by_user_id, get_note_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from v1.userapp.serializers.notes import NoteSerializer, NoteViewSerializer
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()

from v1.userapp.serializers.user import UserViewSerializer
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


# class UserNote(GenericAPIView):
#
#     @is_token_validate
#     @role_required(ADMIN, UTILITY_MASTER, EDIT)
#     def get(self, request, id_string):
#         try:
#             data = {}
#             note_list = []
#             user = get_user_by_id_string(id_string)
#             if user:
#                 data['email'] = user.email
#                 data['id_string'] = id_string
#                 service_type = get_service_type_by_name('User')
#                 if service_type:
#                     user_notes_obj = get_notes_by_user_id(user.id, service_type.id)
#                     if user_notes_obj:
#                         for user_note in user_notes_obj:
#                             serializer = NoteViewSerializer(instance=user_note, context={'request': request})
#                             note_list.append(serializer.data)
#                         data['notes'] = note_list
#                         return Response({
#                             STATE: SUCCESS,
#                             RESULTS: data,
#                         }, status=status.HTTP_200_OK)
#                     else:
#                         return Response({
#                             STATE: ERROR,
#                             RESULTS: NO_NOTES_NOT_FOUND,
#                         }, status=status.HTTP_404_NOT_FOUND)
#                 else:
#                     return Response({
#                         STATE: ERROR,
#                         RESULTS: SERVICE_TYPE_NOT_FOUND,
#                     }, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 return Response({
#                     STATE: EXCEPTION,
#                     RESULTS: ID_STRING_NOT_FOUND,
#                 }, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User notes')
#             return Response({
#                 STATE: EXCEPTION,
#                 RESULTS: '',
#                 ERROR: str(traceback.print_exc(e))
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     @is_token_validate
#     @role_required(ADMIN, UTILITY_MASTER,  EDIT)
#     def post(self, request, id_string):
#         try:
#             data = {}
#             note_list = []
#             user_obj = get_user_by_id_string(id_string)
#             if user_obj:
#                 data['email'] = user_obj.email
#                 data['id_string'] = id_string
#                 service_type = get_service_type_by_name('User')
#                 if service_type:
#                     for note in request.data['notes']:
#                         validate_data = {'identification_id': str(id_string), 'utility_id': request.data['utility_id'], 'module_id': request.data['module_id'], 'sub_module_id': request.data['sub_module_id'], 'service_type_id': str(service_type.id_string), 'note_name' : note['note_name'], 'note_color': note['note_color'], 'note': note['note']}
#                         serializer = NoteSerializer(data=validate_data)
#                         if serializer.is_valid(raise_exception=False):
#                             user_id_string = get_user_from_token(request.headers['token'])
#                             user = get_user_by_id_string(user_id_string)
#                             note_obj = serializer.create(serializer.validated_data, user)
#                             view_serializer = NoteViewSerializer(instance=note_obj, context={'request': request})
#                             note_list.append(view_serializer.data)
#                         else:
#                             return Response({
#                                 STATE: ERROR,
#                                 RESULTS: serializer.errors,
#                             }, status=status.HTTP_400_BAD_REQUEST)
#                     data['notes'] = note_list
#                     return Response({
#                         STATE: SUCCESS,
#                         RESULTS: data,
#                     }, status=status.HTTP_201_CREATED)
#                 else:
#                     raise CustomAPIException(SERVICE_TYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
#             else:
#                 raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User notes')
#             res = self.handle_exception(e)
#             return Response({
#                 STATE: EXCEPTION,
#                 RESULT: str(e),
#             }, status=res.status_code)
#
#     @is_token_validate
#     @role_required(ADMIN, UTILITY_MASTER,  EDIT)
#     def put(self, request, id_string):
#         try:
#             user_obj = get_user_by_id_string(id_string)
#             if user_obj:
#                 service_type = get_service_type_by_name('User')
#                 if service_type:
#                     request.data['identification_id'] = str(id_string)
#                     request.data['service_type_id'] = str(service_type.id_string)
#                     note = get_note_by_id_string(request.data['note_id'])
#                     if note:
#                         serializer = NoteSerializer(data=request.data)
#                         if serializer.is_valid(raise_exception=False):
#                             user_id_string = get_user_from_token(request.headers['token'])
#                             user = get_user_by_id_string(user_id_string)
#                             note_obj = serializer.update(note, serializer.validated_data, user)
#                             view_serializer = NoteViewSerializer(instance=note_obj, context={'request': request})
#                             return Response({
#                                 STATE: SUCCESS,
#                                 RESULTS: view_serializer.data,
#                             }, status=status.HTTP_200_OK)
#                         else:
#                             return Response({
#                                 STATE: ERROR,
#                                 RESULTS: serializer.errors,
#                             }, status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         raise CustomAPIException(NOTES_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
#                 else:
#                     raise CustomAPIException(SERVICE_TYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
#             else:
#                 raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User notes')
#             res = self.handle_exception(e)
#             return Response({
#                 STATE: EXCEPTION,
#                 RESULT: str(e),
#             }, status=res.status_code)




import boto3
from botocore.exceptions import NoCredentialsError
from rest_framework.parsers import FileUploadParser
from boto.s3.connection import S3Connection
from boto.s3.key import Key


class UploadFile(GenericAPIView):

    def post(self, request, format=None):

        print('***********',request.FILES)
        reader_obj = SettingReader.get_s3_credentials()

        file_obj = request.FILES['file']

        conn = S3Connection(reader_obj['AWS_ACCESS_KEY'], reader_obj['AWS_SECRET_KEY'])
        k = Key(conn.get_bucket(reader_obj['AWS_S3_BUCKET']))
        k.key = 'upls/%s/%s.png' % (46, file_obj)
        k.set_contents_from_string(file_obj.read())
        k.set_metadata('Content-Type', 'image/jpeg')
        url = k.generate_url(expires_in=0, query_auth=False, force_http=True)

        print('*****file_obj.read()****',url)
        