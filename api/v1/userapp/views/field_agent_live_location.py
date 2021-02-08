import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from master.models import get_all_users, get_user_by_id_string, is_email_exists,User as UserTbl
from v1.commonapp.common_functions import get_user_from_token,is_token_valid,is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.userapp.models.field_agent_live_location import FieldAgentLiveLocation as FieldAgentLiveLocationTbl
from v1.userapp.serializers.field_agent_live_location import FieldAgentLiveLocationViewSerializer

# API Header
# API end Point: api/v1/resource/live-location/list
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View Resource list
# Usage: Used for Resource list. Get all the records in pagination mode. It also have input params to filter/ search and
# sort in addition to pagination.
# Tables used:  FieldAgentLiveLocation
# Author: Priyanka
# Created on: 22/01/2021


class FieldAgentLiveLocationList(generics.ListAPIView):
    try:
        student_name = request.POST.getlist('student_list')
    except Exception as ex:
        logger().log(ex, 'ERROR')
        # raise APIException

