from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.models.sub_area import SubArea as SubAreaModel, get_sub_area_by_id_string
from v1.commonapp.serializers.sub_area import SubAreaListSerializer, SubAreaViewSerializer, SubAreaSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from django.db import transaction
from v1.commonapp.serializers.premises import PremiseListSerializer, PremiseSerializer, PremiseViewSerializer,PremisesShortViewSerializer
from v1.commonapp.models.premises import Premise as PremiseModel, get_premise_by_id_string
from v1.commonapp.models.sub_area import SubArea as SubAreaModel
from v1.utility.models.utility_region import get_utility_region_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.division import get_division_by_id, get_division_by_id_string
from v1.commonapp.models.city import get_city_by_id, get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id, get_zone_by_id_string
from v1.commonapp.models.area import get_area_by_id, get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id,get_sub_area_by_id_string


# API Header
# API end Point: api/v1/utility/:id_string/subarea/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Premise list
# Usage: API will fetch all Premise list
# Tables used: Premise
# Author: Chinmay
# Created on: 11/11/2020


class PremiseList(generics.ListAPIView):
    try:
        serializer_class = PremiseListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = PremiseModel.objects.filter(utility=utility, is_active=True)
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
                        raise CustomAPIException("Premise not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')


class PremiseShortList(generics.ListAPIView):
    try:
        serializer_class = PremisesShortViewSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = PremiseModel.objects.filter(utility=utility, is_active=True)
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
                        raise CustomAPIException("Premise not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')



# API Header
# API end Point: api/v1/utility/premise
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Premise post
# Usage: API will Post the Premise
# Tables used: Premise
# Author: Chinmay
# Created on: 20/11/2020
class Premise(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                user = get_user_by_id_string(user_id_string)
                serializer = PremiseSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    premise_obj = serializer.create(serializer.validated_data, user)
                    subarea = get_sub_area_by_id(premise_obj.subarea_id)
                    area = get_area_by_id(subarea.area_id)
                    division = get_division_by_id(area.division_id)
                    zone = get_zone_by_id(division.zone_id)
                    city = get_city_by_id(zone.city_id)
                    state = get_state_by_id(city.state_id)
                    country = get_country_by_id(state.country_id)
                    region = get_utility_region_by_id(country.region_id)
                    premise_obj.area_id = area.id
                    premise_obj.division_id = division.id
                    premise_obj.zone_id = zone.id
                    premise_obj.city_id = city.id
                    premise_obj.state_id = state.id
                    premise_obj.country_id = country.id
                    premise_obj.region_id = region.id
                    premise_obj.save()
                    view_serializer = PremiseViewSerializer(instance=premise_obj, context={'request': request})
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
# API end Point: api/v1/utility/premise/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Premise corresponding to the id
# Usage: API will fetch and update Premises for a given id
# Tables used: Premise
# Author: Chinmay
# Created on: 20/1/2020


class PremiseDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            premise = get_premise_by_id_string(id_string)
            if premise:
                serializer = PremiseViewSerializer(instance=premise, context={'request': request})
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
            premise_obj = get_premise_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = premise_obj.name
            if premise_obj:
                serializer = PremiseSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):

                    premise_obj = serializer.update(premise_obj, serializer.validated_data, user)
                    view_serializer = PremiseViewSerializer(instance=premise_obj,
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


