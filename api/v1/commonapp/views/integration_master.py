from rest_framework import status, generics
from api.messages import *
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.commonapp.serializers.integration_master import IntegrationMasterListSerializer, IntegrationMasterSerializer, \
    IntegrationMasterViewSerializer
from v1.commonapp.models.integration_master import IntegrationMaster as IntegrationMasterModel, get_integration_master_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from api.constants import *
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from v1.userapp.decorators import is_token_validate, role_required
from api.messages import *
from master.models import get_user_by_id_string


# API Header
# API end Point: api/v1/:id_string/integration-master/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Integration Master list
# Usage: API will fetch all Integration Master list
# Tables used: Integration Master
# Author: Chinmay
# Created on: 8/2/2020

class IntegrationMasterList(generics.ListAPIView):
    try:
        serializer_class = IntegrationMasterListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = IntegrationMasterModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Integration Details not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')


# API Header
# API end Point: api/v1/utility/integration_master
# API verb: POST
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Integration Details post
# Usage: API will Post the Integration Details
# Tables used: IntegrationMaster
# Author: Chinmay
# Created on: 9/2/2021
class IntegrationMaster(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = IntegrationMasterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                integration_obj = serializer.create(serializer.validated_data, user)
                view_serializer = IntegrationMasterViewSerializer(instance=integration_obj, context={'request': request})
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
# API end Point: api/v1/utility/integration_master/:id_string
# API verb: GET,PUT
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Integration Details corresponding to the id
# Usage: API will fetch and update Integration Details for a given id
# Tables used: IntegrationMaster
# Author: Chinmay
# Created on: 2/9/2021


class IntegrationMasterDetail(GenericAPIView):

    @is_token_validate
    #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request, id_string):
        try:
            integration_master = get_integration_master_by_id_string(id_string)
            if integration_master:
                serializer = IntegrationMasterViewSerializer(instance=integration_master, context={'request': request})
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
            integration_obj = get_integration_master_by_id_string(id_string)
            if "name" not in request.data:
                request.data['name'] = integration_obj.name
            if integration_obj:
                serializer = IntegrationMasterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    integration_obj = serializer.update(integration_obj, serializer.validated_data, user)
                    view_serializer = IntegrationMasterViewSerializer(instance=integration_obj,
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
