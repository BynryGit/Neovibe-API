import traceback
import logging
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_master import UserDetail
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS
from v1.commonapp.common_functions import is_token_valid, get_user, is_authorized
from v1.dispatcher.views.common_functions import is_data_verified
from v1.dispatcher.serializers.service_request import ServiceRequestViewSerializer
from v1.asset.models.asset_master import get_asset_by_id_string
from v1.dispatcher.serializers.service_request import ServiceRequestSerializer,ServiceRequestViewSerializer
from v1.dispatcher.models.service_appointments import get_service_request_by_id_string

# API Header
# API end Point: api/v1/asset/:id_string/service-request
# API verb: POST
# Package: Basic
# Modules: O&M
# Sub Module: Dispatcher
# Interaction: Add Service Request
# Usage: Add
# Tables used: Service Request
# Auther: Priyanka
# Created on: 25/05/2020

class ServiceRequest(GenericAPIView):

    def post(self, request,id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = UserDetail.objects.get(id=5)
                    if is_data_verified(request):
                        asset_obj = get_asset_by_id_string(id_string)
                        serializer = ServiceRequestSerializer(data=request.data)
                        if serializer.is_valid():
                            service_request = serializer.create(serializer.validated_data, user,asset_obj)
                            if service_request:
                                view_serializer = ServiceRequestViewSerializer(instance=service_request,context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
                                }, status=status.HTTP_201_CREATED)
                            else:
                                return Response({
                                    STATE: DUPLICATE,
                                    RESULTS: DATA_ALREADY_EXISTS,
                                }, status=status.HTTP_409_CONFLICT)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
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


# API Header
# API end Point: api/v1/asset/request/:id_string
# API verb: PUT
# Package: Basic
# Modules: O&M
# Sub Module:
# Interaction: Update Service Request
# Usage: Update
# Tables used:  Service Request
# Auther: Priyanka
# Created on: 25/05/2020

# API for Service Request
class ServiceRequestDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    service_request = get_service_request_by_id_string(id_string)
                    if service_request:
                        serializer = ServiceRequestViewSerializer(instance=service_request, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_204_NO_CONTENT)
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
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    user = UserDetail.objects.get(id=2)
                    service_obj = get_service_request_by_id_string(id_string)
                    if service_obj:
                        serializer = ServiceRequestSerializer(data=request.data)
                        if serializer.is_valid():
                            reassign_obj = serializer.update(service_obj, serializer.validated_data, user)
                            view_serializer = ServiceRequestViewSerializer(instance=reassign_obj,context={'request': request})
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
                        }, status=status.HTTP_204_NO_CONTENT)
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

