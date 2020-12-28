from v1.commonapp.serializers.region import TenantRegionSerializer
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required
from master.models import get_user_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from api.constants import *
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.decorators import is_token_validate, role_required
from v1.work_order.serializers.work_order_master import WorkOrderMasterListSerializer,WorkOrderMasterSerializer,WorkOrderMasterViewSerializer
from v1.work_order.models.work_order_master import WorkOrderMaster as WorkOrderMasterModel
from v1.work_order.models.work_order_master import get_work_order_master_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/work_order/utility/:id_string/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Rule list
# Usage: API will fetch all Work Order list
# Tables used: WorkOrderMaster
# Author: Chinmay
# Created on: 22/12/2020

class WorkOrderMasterList(generics.ListAPIView):
    try:
        serializer_class = WorkOrderMasterListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = WorkOrderMasterModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Work Order not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Work Order')


# API Header
# API end Point: api/v1/work_order/service
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Work Order Service post
# Usage: API will Post the Work Order Service
# Tables used: WorkOrderMaster
# Author: Chinmay
# Created on: 22/12/2020
class WorkOrderService(GenericAPIView):

    @is_token_validate
    #@role_required(ADMIN, UTILITY, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = WorkOrderMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                work_order_obj = serializer.create(serializer.validated_data, user)
                view_serializer = WorkOrderMasterViewSerializer(instance=work_order_obj, context={'request': request})
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
            logger().log(e, 'HIGH', module='Admin', sub_module='Work Order')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

# API Header
# API end Point: api/v1/work_order/utility/service/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Service corresponding to the id
# Usage: API will fetch and update Services for a given id
# Tables used: WorkOrderMaster
# Author: Chinmay
# Created on: 22/12/2020

class WorkOrderDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, UTILITY, EDIT)
    def get(self, request, id_string):
        try:
            work_order = get_work_order_master_by_id_string(id_string)
            if work_order:
                serializer = WorkOrderMasterViewSerializer(instance=work_order, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module='Admin', sub_module='Work Order')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, UTILITY, EDIT)
    def put(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            work_order_obj = get_work_order_master_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = work_order_obj.name
            if work_order_obj:
                serializer = WorkOrderMasterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    work_order_obj = serializer.update(work_order_obj, serializer.validated_data, user)
                    view_serializer = WorkOrderMasterViewSerializer(instance=work_order_obj,
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
            logger().log(e, 'HIGH', module='Admin', sub_module='Work Order')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)