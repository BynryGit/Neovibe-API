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
from v1.asset.models.asset_sub_category import AssetSubCategory,get_asset_sub_category_by_id_string
from v1.asset.serializer.sub_category import AssetSubCategoryListSerializer,AssetSubCategoryViewSerializer
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized

# sub_category-list
class AssetSubCategoryList(generics.ListAPIView):
    try:
        serializer_class = AssetSubCategoryListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'tenant__id_string',)
        ordering_fields = ('name', 'tenant',)
        ordering = ('name',)  # always give by default alphabetical order
        search_fields = ('name', 'tenant__name',)

        def get_queryset(self):
            if is_token_valid(0):
                if is_authorized():
                    queryset = AssetSubCategory.objects.filter(is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException



class AssetSubCategoryDetail(GenericAPIView):
    def get(self,request,id_string):
        try:
            asset_sub_category = get_asset_sub_category_by_id_string(id_string)
            if asset_sub_category:
                serializer = AssetSubCategoryViewSerializer(instance=asset_sub_category,context={'request':request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
