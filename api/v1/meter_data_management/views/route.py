from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
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
from v1.meter_data_management.serializers.route import RouteViewSerializer, RouteSerializer, RouteListSerializer, \
    RouteShortViewSerializer
from v1.meter_data_management.models.route import Route as RouteModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.meter_data_management.models.route import get_route_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from api.messages import ROUTE_NOT_FOUND, SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from api.constants import *
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id_string
from v1.commonapp.models.division import get_division_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from datetime import datetime, timedelta

# API Header
# API end Point: api/v1/utility/:id_string/route/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Route list
# Usage: API will fetch all Route list
# Tables used: Route
# Author: Chinmay
# Created on: 14/1/2021


class RouteList(generics.ListAPIView):
    try:
        serializer_class = RouteListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = RouteModel.objects.filter(utility=utility, is_active=True, created_date__gte=datetime.now() - timedelta(days=180))
                    if 'city_id' in self.request.query_params:
                        city = get_city_by_id_string(self.request.query_params['city_id'])
                        queryset = queryset.filter(city_id=city.id)
                    if 'zone_id' in self.request.query_params:
                        zone = get_zone_by_id_string(self.request.query_params['zone_id'])
                        queryset = queryset.filter(zone_id=zone.id)
                    if 'division_id' in self.request.query_params:
                        division = get_division_by_id_string(self.request.query_params['division_id'])
                        queryset = queryset.filter(division_id=division.id)
                    if 'area_id' in self.request.query_params:
                        area = get_area_by_id_string(self.request.query_params['area_id'])
                        queryset = queryset.filter(area_id=area.id)
                    if 'subarea_id' in self.request.query_params:
                        sub_area = get_sub_area_by_id_string(self.request.query_params['subarea_id'])
                        queryset = queryset.filter(subarea_id=sub_area.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(ROUTE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


class RouteShortList(generics.ListAPIView):
    try:
        serializer_class = RouteShortViewSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = RouteModel.objects.filter(utility=utility, is_active=True, created_date__gte=datetime.now() - timedelta(days=180))
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(ROUTE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


# API Header
# API end Point: api/v1/meter-data/route
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Route post
# Usage: API will Post the Route
# Tables used: Route
# Author: Chinmay
# Created on: 14/1/2021





class Route(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request, id_string):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                serializer = RouteSerializer(data=request.data)
                utility = get_utility_by_id_string(self.kwargs['id_string'])
                queryset = RouteModel.objects.filter(utility=utility,is_active=True)
                premise_id_strings = [item.premises_json[0]['id_string'] for item in queryset]
                # for i in queryset:
                #     print("QURY",queryset)
                if serializer.is_valid(raise_exception=False):                  
                    # print("Route Object", serializer.validated_data['route_json'])
                    for premises_id_string in serializer.validated_data['premises_json']:
                        print("JUJUJ", premises_id_string['id_string'])
                        if premises_id_string['id_string'] in premise_id_strings:
                            return Response({
                                STATE: ERROR,
                                RESULTS: 'CANNOT_ENTER_DUPLICATE_PREMISE',
                            }, status=status.HTTP_409_CONFLICT) 
                    route_obj = serializer.create(serializer.validated_data, user)
                    view_serializer = RouteViewSerializer(instance=route_obj, context={'request': request})
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
# API end Point: api/v1/meter-data/route/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Route corresponding to the id
# Usage: API will fetch and update Route for a given id
# Tables used: Route
# Author: Chinmay
# Created on: 14/1/2021


class RouteDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            route = get_route_by_id_string(id_string)
            if route:
                serializer = RouteViewSerializer(instance=route, context={'request': request})
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
            route_obj = get_route_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = route_obj.name
            if route_obj:
                serializer = RouteSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    route_obj = serializer.update(route_obj, serializer.validated_data, user)
                    view_serializer = RouteViewSerializer(instance=route_obj,
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
