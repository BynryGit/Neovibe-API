from v1.commonapp.models.notification_subtype import NotificationSubType as NotificationSubTypeModel, get_notification_subtype_by_id_string
from v1.commonapp.serializers.notification_subtype import NotificationSubTypeListSerializer, NotificationSubTypeSerializer, \
    NotificationSubTypeViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/utility/:id_string/notification_subtype/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: NotificationSubType list
# Usage: API will fetch all NotificationSubType list
# Tables used: NotificationSubType
# Author: Chinmay
# Created on: 29/1/2021

class NotificationSubTypeList(generics.ListAPIView):
    try:
        serializer_class = NotificationSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = NotificationSubTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Notification SubType not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/utility/notification_subtype
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: NotificationSubType post
# Usage: API will Post the NotificationSubType
# Tables used: NotificationSubType
# Author: Chinmay
# Created on: 29/1/2021
class NotificationSubType(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = NotificationSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                notification_subtype_obj = serializer.create(serializer.validated_data, user)
                view_serializer = NotificationSubTypeViewSerializer(instance=notification_subtype_obj, context={'request': request})
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
# API end Point: api/v1/utility/notification_subtype/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: NotificationSubType corresponding to the id
# Usage: API will fetch and update NotificationSubType for a given id
# Tables used: NotificationSubType
# Author: Chinmay
# Created on: 29/1/2020


class NotificationSubTypeDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            notification_subtype = get_notification_subtype_by_id_string(id_string)
            if notification_subtype:
                serializer = NotificationSubTypeViewSerializer(instance=notification_subtype, context={'request': request})
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
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            notification_subtype_obj = get_notification_subtype_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = notification_subtype_obj.name
            if notification_subtype_obj:
                serializer = NotificationSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    notification_subtype_obj = serializer.update(notification_subtype_obj, serializer.validated_data, user)
                    view_serializer = NotificationSubTypeViewSerializer(instance=notification_subtype_obj,
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