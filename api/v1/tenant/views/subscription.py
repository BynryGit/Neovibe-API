import traceback
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.tenant.models.tenant_subscription import TenantSubscription as subscriptionTbl
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.tenant.serializers.subscription import SubscriptionListSerializer, SubscriptionViewSerializer, \
     SubscriptionSerializer
from v1.tenant.models.tenant_subscription import get_subscription_by_id_string
from v1.tenant.views.common_functions import is_data_verified, is_subscription_data_verified
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA, RESULTS, DUPLICATE


# API Header
# API end Point: api/v1/tenant/subscription/list
# API verb: GET
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Tenant list
# Usage: API will fetch required data for Tenant list
# Tables used: 1.1 Tenant Master
# Author: Gauri Deshmukh
# Created on: 21/05/2020
from v1.userapp.models.user_master import UserDetail


class SubscriptionList(generics.ListAPIView):
    serializer_class = SubscriptionListSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('subscription_plan_id', 'id_string',)
    ordering_fields = ('subscription_plan_id', 'id_string')
    ordering = ('created_date')  # always give by default alphabetical order
    search_fields = ('subscription_plan_id')

    def get_queryset(self):
        queryset = subscriptionTbl.objects.filter(is_active=True)
        return queryset



# API Header
# API end Point: api/v1/tenant/subscription
# API verb: POST
# Package: Basic
# Modules: Tenant
# Sub Module: Subscription
# Interaction: Add Tenant Subscription
# Usage: Add Tenant Subscription in the system
# Tables used:  Tenant Subscription
# Auther: Gauri Deshmukh
# Created on: 21/5/2020

class Subscription(GenericAPIView):

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    user = UserDetail.objects.get(id = 2)
                    if is_subscription_data_verified(request):
                    #Request data verification end
                        duplicate_subscription_obj = subscriptionTbl.objects.filter(subscription_plan_id=request.data['subscription_plan_id'])
                        if duplicate_subscription_obj:
                            return Response({
                                STATE: DUPLICATE,
                            }, status=status.HTTP_404_NOT_FOUND)
                        else:
                            serializer = SubscriptionSerializer(data=request.data)
                        if serializer.is_valid():
#                            tenant_obj = serializer.create(serializer.validated_data, user)
                            subscription_obj = serializer.create(serializer.validated_data)
                            view_serializer = SubscriptionViewSerializer(instance=subscription_obj, context={'request': request})
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
            # logger().log(e, 'ERROR', user='Exception', name='Testing')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API Header
# API end Point: api/v1/tenant/subscription/:id_string
# API verb: Put,Get
# Package: Basic
# Modules: All
# Sub Module: All
# Interaction: Get Tenant, Update Tenant Subscription
# Usage: Add and Update Tenant Subscription in the system
# Tables used:  Tenant Subscription
# Auther: Gauri Deshmukh
# Created on: 21/5/2020

class SubscriptionDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    tenant_subscription = get_subscription_by_id_string(id_string)
                    if tenant_subscription:
                        serializer = SubscriptionViewSerializer(instance=tenant_subscription, context={'request': request})
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
                    if is_subscription_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        # user = UserDetail.objects.get(id=2)
                        subscription_obj = get_subscription_by_id_string(id_string)

                        if subscription_obj:
                            serializer = SubscriptionSerializer(data=request.data)
                            print("Here");
                            if serializer.is_valid(request.data):

                                subscription_obj = serializer.update(subscription_obj, serializer.validated_data)

                                view_serializer = SubscriptionViewSerializer(instance=subscription_obj,
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


