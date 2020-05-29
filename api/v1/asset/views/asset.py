__author__ = "Priyanka"

import traceback
import logging
from datetime import datetime
from django.db import transaction
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.asset.views.common_function import is_data_verified
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.asset.serializer.asset import AssetListSerializer,AssetViewSerializer,AssetSerializer
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.asset.models.asset_master import Asset as AssetTbl,get_asset_by_id_string
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS,DUPLICATE,DATA_ALREADY_EXISTS
from v1.userapp.models.user_master import UserDetail



# API Header
# API end Point: api/v1/asset/list
# API verb: GET
# Package: Basic
# Modules: o&M
# Sub Module: Asset
# Interaction: Asset List
# Usage: API will fetch required data for Asset list
# Tables used:  Asset Master
# Author: Priyanka Kachare
# Created on: 21/05/2020

# Api for getting Asset  list

class AssetList(generics.ListAPIView):
    try:
        serializer_class = AssetListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string','asset_no')
        ordering_fields = ('name','asset_no')
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name','asset_no')

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = AssetTbl.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException


# API Header
# API end Point: api/v1/asset
# API verb: POST
# Package: Basic
# Modules: O&M
# Sub Module: Asset
# Interaction: Add Asset
# Usage: Add
# Tables used:  Asset Master
# Auther: Priyanka
# Created on: 20/05/2020

class Asset(GenericAPIView):

    def post(self, request):

        try:
            if is_token_valid(1):
                if is_authorized():
                    user = UserDetail.objects.get(id=5)
                    if is_data_verified(request):
                        serializer = AssetSerializer(data=request.data)
                        if serializer.is_valid():
                            asset_obj = serializer.create(serializer.validated_data, user)
                            if asset_obj:
                                view_serializer = AssetViewSerializer(instance=asset_obj,context={'request': request})
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
# API end Point: api/v1/asset/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: O&M
# Sub Module: Asset
# Interaction: View  and Update Asset
# Usage: View,Update
# Tables used:  Asset Master
# Auther: Priyanka
# Created on: 21/05/2020

# API for  edit, view Asset details
class AssetDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    asset = get_asset_by_id_string(id_string)
                    if asset:
                        serializer = AssetViewSerializer(instance=asset, context={'request': request})
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
                    asset = get_asset_by_id_string(id_string)
                    if asset:
                        serializer = AssetSerializer(data=request.data)
                        if serializer.is_valid():
                            asset_obj = serializer.update(asset, serializer.validated_data, user)
                            view_serializer = AssetViewSerializer(instance=asset_obj,context={'request': request})
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

