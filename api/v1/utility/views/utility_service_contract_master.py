from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.userapp.decorators import is_token_validate
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_service_contract_master import UtilityServiceContractMaster, \
    get_utility_service_contract_master_by_id_string
from v1.utility.serializers.utility_service_contract_master import UtilityServiceContractMasterListSerializer, \
    UtilityServiceContractMasterDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class UtilityServiceContractMasterList(generics.ListAPIView):
    try:
        serializer_class = UtilityServiceContractMasterListSerializer
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
                    queryset = UtilityServiceContractMaster.objects.filter(utility=utility, is_active=True)
                    if 'consumer_sub_category_id' in self.request.query_params:
                        sub_category = get_consumer_sub_category_by_id_string(self.request.query_params['consumer_sub_category_id'])
                        queryset = queryset.filter(consumer_sub_category_id=sub_category.id)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Utility service contracts not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Utility', sub_module='Utility')


class UtilityServiceContractMasterDetail(GenericAPIView):

        # @is_token_validate
        # @role_required(ADMIN, UTILITY, VIEW)
        def get(self, request, id_string):
            try:
                contract = get_utility_service_contract_master_by_id_string(id_string)
                if contract:
                    serializer = UtilityServiceContractMasterDetailSerializer(instance=contract, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULT: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULT: UTILITY_SERVICE_CONTRACT_NOT_FOUND,
                    }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger().log(e, 'MEDIUM', module='Utility', sub_module='Utility')
                res = self.handle_exception(e)
                return Response({
                    STATE: EXCEPTION,
                    RESULT: str(e),
                }, status=res.status_code)
