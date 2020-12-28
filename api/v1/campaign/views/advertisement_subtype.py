from rest_framework import generics, status
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.campaign.serializers.advertisement_subtype import AdvertisementSubTypeListSerializer,AdvertisementSubTypeViewSerializer, AdvertisementSubTypeSerializer
from v1.campaign.models.advertisement_subtype import AdvertisementSubType as AdvertisementSubTypeModel ,get_advert_subtype_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, get_payload, is_authorized, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException


# API Header
# API end Point: api/v1/campaign/:id_string/advertisementsubtype/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Campaign
# Interaction: Campaign Advertisement Sub Type list
# Usage: API will fetch all Advertisemetn Sub Type list
# Tables used: Advertisment Sub Type
# Author: Chinmay
# Created on: 26/11/2020



# 'advert-type/list'
class AdvertisementSubTypeList(generics.ListAPIView):
    try:
        serializer_class = AdvertisementSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = AdvertisementSubTypeModel.objects.filter(utility=utility)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Advertisement Sub Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Campaign')






# API Header
# API end Point: api/v1/campaign/:id_string/advertisementsubtype
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: advertisementsubtype corresponding to the id
# Usage: API will fetch and update advertisementsubtype for a given id
# Tables used: AdvertisementSubType
# Author: Chinmay
# Created on: 26/11/2020


class AdvertisementSubTypeDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            advertisement_subtype = get_advert_subtype_by_id_string(id_string)
            if advertisement_subtype:
                serializer = AdvertisementSubTypeViewSerializer(instance=advertisement_subtype, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Campaign')
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
            advertisement_subtype_obj = get_advert_subtype_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = advertisement_subtype_obj.name
            if advertisement_subtype_obj:
                serializer = AdvertisementSubTypeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    advertisement_subtype_obj = serializer.update(advertisement_subtype_obj, serializer.validated_data, user)
                    view_serializer = AdvertisementSubTypeSerializer(instance=advertisement_subtype_obj,
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
            logger().log(e, 'HIGH', module='Admin', sub_module='Campaign')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)


# API Header
# API end Point: api/v1/advertisementtype
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Advertisement Post
# Usage: API will POST Advertisements into database
# Tables used: Advertisement Type
# Author: Chinmay
# Created on: 26/11/2020
class AdvertisementSubType(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = AdvertisementSubTypeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                advertisement_subtype_obj = serializer.create(serializer.validated_data, user)
                view_serializer = AdvertisementSubTypeViewSerializer(instance=advertisement_subtype_obj, context={'request': request})
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
            logger().log(e, 'HIGH', module='Admin', sub_module='Campaign')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)