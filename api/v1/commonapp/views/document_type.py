import traceback
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.serializers.region import TenantRegionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.serializers.document_type import DocumentTypeSerializer, DocumentTypeViewSerializer, \
    DocumentTypeListSerializer
from v1.commonapp.models.document_type import DocumentType as DocumentTypeModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.document_type import get_document_type_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/:id_string/document_type/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Document Type list
# Usage: API will fetch all Document Type list
# Tables used: DocumentType
# Author: Chinmay
# Created on: 22/1/2021


class DocumentTypeList(generics.ListAPIView):
    try:
        serializer_class = DocumentTypeSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = DocumentTypeModel.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("DocumentType not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/document_type
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: DocumentType Post
# Usage: API will POST DocumentType into database
# Tables used: DocumentType
# Author: Chinmay
# Created on: 22/1/2021
class DocumentType(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            # if 'document_type_id' in request.data:
            #     document_type_id = request.data.pop('document_type_id')
            serializer = DocumentTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                document_type_obj = serializer.create(serializer.validated_data, user)
                # if document_type_obj:
                #     if document_type_id:
                #         for utility_mod_sub in document_type_id:
                #             utility_module = utility_mod_sub['utility_module']
                #             utility_module['tenant'] = document_type_obj.tenant.id_string
                #             utility_module['utility'] = document_type_obj.id_string
                #             utility_module_serializer = UtilityModuleSerializer(data=utility_module)
                view_serializer = DocumentTypeViewSerializer(instance=document_type_obj, context={'request': request})
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
# API end Point: api/v1/:id_string/document_type
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: DocumentType corresponding to the id
# Usage: API will fetch and update DocumentType for a given id
# Tables used: DocumentType
# Author: Chinmay
# Created on: 22/1/2021


class DocumentTypeDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            document_type = get_document_type_by_id_string(id_string)
            if document_type:
                serializer = DocumentTypeViewSerializer(instance=document_type, context={'request': request})
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
            document_type_obj = get_document_type_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = document_type_obj.name
            if document_type_obj:
                serializer = DocumentTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    document_type_obj = serializer.update(document_type_obj, serializer.validated_data, user)
                    view_serializer = DocumentTypeViewSerializer(instance=document_type_obj,
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
