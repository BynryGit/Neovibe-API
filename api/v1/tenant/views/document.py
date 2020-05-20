__author__ = "Gauri"

import traceback
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.document import get_documents_by_tenant_id_string, get_document_by_id_string
from v1.commonapp.views.logger import logger
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.serializers.document import DocumentSerializer


# API Header
# API end Point: api/v1/tenant/id_string/documents
# API verb: GET, POST
# Package: Basic
# Modules: Tenant
# Sub Module: Document
# Interaction: for get and add Tenant document
# Usage: API will fetch and add all documents under Tenant.
# Tables used:  Document
# Author: Gauri Deshmukh
# Created on: 13/05/2020


class TenantDocumentList(GenericAPIView):

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    tenant_document_obj = get_documents_by_tenant_id_string(id_string)
                    if tenant_document_obj:
                        serializer = DocumentSerializer(tenant_document_obj, many=True, context={'request': request})
                        if serializer.is_valid():
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request,id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    tenant_obj = get_tenant_by_id_string(id_string)
                    if tenant_obj:
                        serializer = DocumentSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.validated_data['utility']=tenant_obj.id
                            serializer.create(serializer.validated_data, request.user)
                            return Response({
                                STATE: SUCCESS,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/utility/document/id_string
# API verb: GET, PUT
# Package: Basic
# Modules: Utility
# Sub Module: Document
# Interaction: for get and edit utility document
# Usage: API will fetch and edit documents under utility.
# Tables used: 2.12.13 Document
# Author: Gauri Deshmukh
# Created on: 13/05/2020


class TenantDocumentDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                # Checking authorization end

                    tenant_document_obj = get_document_by_id_string(id_string)
                    if tenant_document_obj:
                        serializer = DocumentSerializer(tenant_document_obj,context={'request':request})
                        if serializer.is_valid():
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.data,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request,id_string):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # payload = get_payload(request.headers['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    tenant_document_obj = get_document_by_id_string(id_string)
                    if tenant_document_obj:
                        serializer = DocumentSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.create(serializer.validated_data, request.user)
                            return Response({
                                STATE: SUCCESS,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(ex))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)