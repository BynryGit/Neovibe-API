import traceback
from v1.commonapp.views.logger import logger
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.asset.models.asset_category import AssetCategory,get_asset_category_by_id_string
from v1.asset.serializer.category import AssetCategoryListSerializer,AssetCategoryViewSerializer
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized

# category-list
class AssetCategoryList(generics.ListAPIView):
    try:
        serializer_class = AssetCategoryListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = AssetCategory.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException



class AssetCategoryDetail(GenericAPIView):
    def get(self,request,id_string):
        try:
            asset_category = get_asset_category_by_id_string(id_string)
            if asset_category:
                serializer = AssetCategoryViewSerializer(instance=asset_category,context={'request':request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
