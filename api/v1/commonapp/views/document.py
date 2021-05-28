from api.constants import *
from api.messages import *
from api.messages import *
from datetime import datetime
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from master.models import get_user_by_id_string
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token, validate_user_data
from v1.commonapp.models.document import Document as DocumentModel
from v1.commonapp.models.document import get_document_by_id_string, Document as DocumentTbl
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.commonapp.serializers.document import DocumentListSerializer, DocumentSerializer, DocumentViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.views.settings_reader import SettingReader
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_filter_backend import CustomFilter
import os
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
setting_reader = SettingReader()

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys
import boto3
import boto.s3.connection

# API Header
# API end Point: api/v1/utility/:id_string/document/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Documents list
# Usage: API will fetch all Documents list
# Tables used: Document
# Author: Chinmay
# Created on: 22/1/2021
latest_record = []


class DocumentList(generics.ListAPIView):
    try:
        serializer_class = DocumentListSerializer
        pagination_class = StandardResultsSetPagination
        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    latest_record = DocumentModel.objects.latest('created_date')
                    # queryset = DocumentModel.objects.filter(utility=utility, is_active=True,
                    #                                         document_generated_name=latest_record)
                    queryset = DocumentModel.objects.filter(utility=utility, is_active=True)
                    print("LATEST", latest_record)

                    queryset = DocumentModel.objects.filter(utility=utility, is_active=True)
                    if 'consumer_id' in self.request.query_params:
                        id = get_consumer_by_id_string(self.request.query_params['consumer_id']).id
                        module_obj = get_module_by_key('CX')
                        sub_module_obj = get_sub_module_by_key('CONSUMER')
                        queryset = queryset.filter(object_id=id, module_id=module_obj, sub_module_id=sub_module_obj)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Document not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


class GlobalDocumentList(generics.ListAPIView):
    try:
        serializer_class = DocumentListSerializer
        pagination_class = StandardResultsSetPagination
        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = DocumentModel.objects.filter(is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Document not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/document
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Document post
# Usage: API will Post the Document
# Tables used: Document
# Author: Chinmay
# Created on: 22/1/2021
class Document(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                document_obj = serializer.create(serializer.validated_data, user)
                view_serializer = DocumentViewSerializer(instance=document_obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/utility/document/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Document corresponding to the id
# Usage: API will fetch and update documents for a given id
# Tables used: Document
# Author: Chinmay
# Created on: 22/1/2020


class DocumentDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            document = get_document_by_id_string(id_string)
            if document:
                serializer = DocumentViewSerializer(instance=document, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            document_obj = get_document_by_id_string(id_string)
            if "document_name" not in request.data:
                request.data['document_name'] = document_obj.document_name
            if document_obj:
                serializer = DocumentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    document_obj = serializer.update(document_obj, serializer.validated_data, user)
                    view_serializer = DocumentViewSerializer(instance=document_obj,
                                                             context={'request': request})
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
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/document/upload
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: User
# Interaction: Save Document
# Usage: API will save the documents
# Tables used: Document
# Author: Priyanka
# Created on: 25/02/2021


class UploadDocument(GenericAPIView):

    def post(self, request, format=None):
        try:
            # getting object_id start
            user_obj = validate_user_data(request.data)
            # getting object_id end

            utility_obj = get_utility_by_id_string(request.data["utility_id_string"])
            module_obj = get_module_by_id_string(request.data["module_id_string"])
            sub_module_obj = get_sub_module_by_id_string(request.data["sub_module_id_string"])

            # getting S3 credentials from SettingReader 
            reader_obj = SettingReader.get_s3_credentials()
            print("READER OBJ")
            file_obj = request.FILES['file']

            # establish connection with AWS s3 & Upload file/image on s3 start
            conn = S3Connection(reader_obj['AWS_ACCESS_KEY'], reader_obj['AWS_SECRET_KEY'])
            k = Key(conn.get_bucket(reader_obj['AWS_S3_BUCKET']))

            # Storing images module wise
            if module_obj.name == 'ADMIN' and os.environ["smart360_env"] == 'dev':
                today = datetime.now()
                month = today.strftime('%B')
                year = today.strftime('%Y')
                k.key = 'Development/' + str(utility_obj.tenant) + '/' + str(utility_obj.name) + '/' + str(
                    module_obj.name) + '/' + str(
                    year) + '/' + str(month) + '/' + '/%s/%s' % ('', file_obj)
                k.set_contents_from_string(file_obj.read())
                k.set_metadata('Content-Type', 'image/jpeg')
                # establish connection with AWS s3 & Upload file/image on s3 end

                # Create Normal URL
                url = k.generate_url(expires_in=0, query_auth=False, force_http=True)

                s3 = boto3.client('s3', aws_access_key_id=reader_obj['AWS_ACCESS_KEY'],
                                  aws_secret_access_key=reader_obj['AWS_SECRET_KEY'])

                # Create Signed URL
                signed_url = s3.generate_presigned_url('get_object', Params={'Bucket': reader_obj['AWS_S3_BUCKET'],
                                                                             'Key': 'Development/' + str(
                                                                                 utility_obj.tenant) + '/' + str(
                                                                                 utility_obj.name) + '/' +
                                                                                    str(module_obj.name) + '/' + str(
                                                                                 year) + '/' + str(month) + '/' + str(
                                                                                 file_obj)}, ExpiresIn=3600,
                                                       HttpMethod='GET')

                # Split to store auth details in separate field
                auth_details = signed_url.split(sep="?")

            # Save value into Document Table
            document = DocumentTbl()
            if DocumentTbl.objects.filter(document_name=file_obj).exists():
                    raise CustomAPIException("Document Already Exists", status_code=status.HTTP_409_CONFLICT)
                    pass
            else:
                document.tenant = utility_obj.tenant
                document.utility = utility_obj
                document.document_auth_details = auth_details[1]
                document.last_auth_generated = datetime.utcnow()
                document.auth_time_span = "7"
                document.module_id = module_obj.id
                document.sub_module_id = sub_module_obj.id
                document.document_type_id = 1
                document.document_sub_type_id = 1
                document.object_id = user_obj['object_id']
                document.document_generated_name = url
                document.document_name = file_obj
                document.is_active = True
                document.save()
            return Response({
                STATE: SUCCESS,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='Utility')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)
