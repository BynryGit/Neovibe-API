from rest_framework import generics, status
from rest_framework.generics import GenericAPIView

from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.consumer.models.consumer_category import ConsumerCategory as ConsumerCategoryModel, \
    get_consumer_category_by_id_string
from v1.consumer.serializers.consumer_category import ConsumerCategoryListSerializer, ConsumerCategoryViewSerializer, \
    ConsumerCategorySerializer
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from master.models import get_user_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/consumer/utility/:id_string/category/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Consumer Category list
# Usage: API will fetch all Consumer Category List
# Tables used: Consumer Category
# Author: Chinmay
# Created on: 1/12/2020
class ConsumerCategoryList(generics.ListAPIView):
    try:
        serializer_class = ConsumerCategoryListSerializer
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
                    queryset = ConsumerCategoryModel.objects.filter(utility=utility, is_active=True)
                    queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer Category not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/consumer/category
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Survey post
# Usage: API will Post the Surveys
# Tables used: Survey Type
# Author: Chinmay
# Created on: 28/11/2020
class ConsumerCategory(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ConsumerCategorySerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                consumer_category_obj = serializer.create(serializer.validated_data, user)
                view_serializer = ConsumerCategoryViewSerializer(instance=consumer_category_obj,
                                                                 context={'request': request})
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
# API end Point: api/v1/consumer/category/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Consumer Category corresponding to the id
# Usage: API will fetch and update Consumer Category for a given id
# Tables used: Consumer Categories
# Author: Chinmay
# Created on: 1/11/2020


class ConsumerCategoryDetail(GenericAPIView):
    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            consumer_category = get_consumer_category_by_id_string(id_string)
            if consumer_category:
                serializer = ConsumerCategoryViewSerializer(instance=consumer_category, context={'request': request})
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
            consumer_category_obj = get_consumer_category_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = consumer_category_obj.name
            if consumer_category_obj:
                serializer = ConsumerCategorySerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    consumer_category_obj = serializer.update(consumer_category_obj, serializer.validated_data, user)
                    view_serializer = ConsumerCategoryViewSerializer(instance=consumer_category_obj,
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
