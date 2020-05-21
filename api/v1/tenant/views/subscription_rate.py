import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_subscription_plan import TenantSubscriptionPlan as subscriptionPlanTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.tenant.serializers.subscription_plan import SubscriptionPlanListSerializer, SubscriptionPlanViewSerializer, \
     SubscriptionPlanSerializer
from v1.tenant.models.tenant_subscription_plan import get_subscription_plan_by_id_string
from v1.tenant.views.common_functions import is_data_verified
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS, DUPLICATE


# API Header
# API end Point: api/v1/tenant/subscription-plan/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant Subscription plan list
# Usage: API will fetch required data for Tenant Subscription plan list
# Tables used: 1.1 Tenant Subscription plan
# Author: Gauri Deshmukh
# Created on: 21/05/2020

class SubscriptionList(generics.ListAPIView):
    serializer_class = SubscriptionPlanListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('subscription_plan_id', 'id_string',)
    ordering_fields = ('subscription_plan_id', 'id_string')
    ordering = ('created_date')  # always give by default alphabetical order
    search_fields = ('subscription_plan_id')

    def get_queryset(self):
        queryset = subscriptionPlanTbl.objects.filter(is_active=True)
        return queryset



# API Header
# API end Point: api/v1/tenant/subscription-plan
# API verb: POST
# Package: Basic
# Modules: Tenant
# Sub Module: Subscription Plan
# Interaction: Add Tenant Subscriptionn Plan
# Usage: Add Tenant Subscription Plan in the system
# Tables used:  Tenant Subscription Plan
# Auther: Gauri Deshmukh
# Created on: 21/5/2020

class SubscriptionPlan(GenericAPIView):

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    #user = UserDetail.objects.get(id = 2)
                    if is_data_verified(request):
                    # Request data verification end
                        duplicate_subscription_plan_obj = subscriptionPlanTbl.objects.filter(id_string=request.data["id_string"],
                                                                              subscription_plan=request.data['subscription_plan_id'])
                        if duplicate_subscription_plan_obj:
                            return Response({
                                STATE: DUPLICATE,
                            }, status=status.HTTP_404_NOT_FOUND)
                        else:
                            serializer = SubscriptionPlanSerializer(data=request.data)
                        if serializer.is_valid():
#                            tenant_obj = serializer.create(serializer.validated_data, user)
                            subscription_plan_obj = serializer.create(serializer.validated_data)
                            view_serializer = SubscriptionPlanViewSerializer(instance=subscription_plan_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
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
            traceback.print_exc(e)
            logger().log(e, 'ERROR', user='Exception', name='Testing')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API Header
# API end Point: api/v1/tenant/subscription-plan/:id_string
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module: Subscription Plan
# Interaction: Get Tenant, Update Tenant Subscription Plan
# Usage: Add and Update Tenant Subscription Plan in the system
# Tables used:  Tenant Subscription plan
# Auther: Gauri Deshmukh
# Created on: 21/5/2020

class SubscriptionPlaneDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    tenant_subscription_plan = get_subscription_plan_by_id_string(id_string)
                    if tenant_subscription_plan:
                        serializer = SubscriptionPlanViewSerializer(instance=tenant_subscription_plan, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            DATA: serializer.data,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            STATE: EXCEPTION,
                            DATA: '',
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # logger().log(e, 'ERROR', user='Get Tenant Exception ', name='Tenant issue')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        # user = UserDetail.objects.get(id=2)
                        subscription_plan_obj = get_subscription_plan_by_id_string(id_string)

                        if subscription_plan_obj:
                            serializer = SubscriptionPlanSerializer(data=request.data)
                            print("Here");
                            if serializer.is_valid(request.data):

                                subscription_plan_obj = serializer.update(subscription_plan_obj, serializer.validated_data)

                                view_serializer = SubscriptionPlanViewSerializer(instance=subscription_plan_obj,
                                                                             context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
                                }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                        # Save basic details start
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
            # logger().log(e, 'ERROR', user='Tenant update exception', name='Tenant')
            print("#######################",e)
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


