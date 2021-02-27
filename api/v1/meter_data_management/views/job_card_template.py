__author__ = "chinmay"

from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException, CustomAPIException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.serializers.job_card_template import JobCardTemplateListSerializer, \
    JobCardTemplateViewSerializer, JobCardTemplateSerializer
from v1.meter_data_management.models.job_card_template import \
    JobCardTemplate as JobCardTemplateModel, get_job_card_template_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string

from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/meter_data/:id_string/job-card-template/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Job card template list
# Usage: API will fetch all Job card template list
# Tables used: JobCardTemplate
# Author: Chinmay
# Created on: 25/2/2020


class JobCardTemplateList(generics.ListAPIView):
    try:
        serializer_class = JobCardTemplateListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = JobCardTemplateModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Template not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/meter-data/job-task-template
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Job Task Template post
# Usage: API will Post the Job Task
# Tables used: JobTask
# Author: Chinmay
# Created on: 25/2/2021
class JobCardTemplate(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = JobCardTemplateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                template_obj = serializer.create(serializer.validated_data, user)
                view_serializer = JobCardTemplateViewSerializer(instance=template_obj, context={'request': request})
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
# API end Point: api/v1/meter-data/jab-task/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Job Task corresponding to the id
# Usage: API will fetch and update Job Task for a given id
# Tables used: JobCardTemplate
# Author: Chinmay
# Created on: 26/2/2020


class JobCardTemplateDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            template_obj = get_job_card_template_by_id_string(id_string)
            if template_obj:
                serializer = JobCardTemplateViewSerializer(instance=template_obj, context={'request': request})
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
            template_obj_obj = get_job_card_template_by_id_string(id_string)
            if "task_name" not in request.data:
                request.data['task_name'] = template_obj_obj.name
            if template_obj_obj:
                serializer = JobCardTemplateSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    template_obj_obj = serializer.update(template_obj_obj, serializer.validated_data, user)
                    view_serializer = JobCardTemplateViewSerializer(instance=template_obj_obj,
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
