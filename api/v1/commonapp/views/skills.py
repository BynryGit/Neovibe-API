__author__ = "Priyanka"

from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.skills import Skills as SkillTableModel
from v1.commonapp.serializers.skill import GetSkillSerializer,SkillListSerializer,SkillViewSerializer,SkillSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_master import get_utility_by_id_string
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from master.models import get_user_by_id_string
from v1.commonapp.models.skills import get_skill_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import *
from api.constants import *
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.pagination import StandardResultsSetPagination



class SkillsList(generics.ListAPIView):
    try:
        serializer_class = SkillListSerializer
        pagination_class = StandardResultsSetPagination



        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = SkillTableModel.objects.filter(utility = utility, is_active = True)

                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Skill not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Commonapp', sub_module = 'Commonapp')

# API Header
# API end Point: api/v1/utility/skill
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Skill post
# Usage: API will Post the skill
# Tables used: Skill
# Author: Chinmay
# Created on: 24/11/2020
class Skill(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = SkillSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                skill_obj = serializer.create(serializer.validated_data, user)
                view_serializer = SkillViewSerializer(instance=skill_obj, context={'request': request})
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
# API end Point: api/v1/utility/skill/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Skills corresponding to the id
# Usage: API will fetch and update Skills for a given id
# Tables used: SKills
# Author: Chinmay
# Created on: 24/11/2020


class SkillDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            skill = get_skill_by_id_string(id_string)
            if skill:
                serializer = SkillViewSerializer(instance=skill, context={'request': request})
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
            skill_obj = get_skill_by_id_string(id_string)
            if "skill" not in request.data:
                request.data['skill'] = skill_obj.name
            if skill_obj:
                serializer = SkillSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    skill_obj = serializer.update(skill_obj, serializer.validated_data, user)
                    view_serializer = SkillViewSerializer(instance=skill_obj,
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

