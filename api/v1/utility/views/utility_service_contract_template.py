from v1.utility.models.utility_service_contract_template import UtilityServiceContractTemplate as UtilityServiceContractTemplateModel
from v1.utility.serializers.utility_service_contract_template import UtilityServiceContractTemplateListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.models.city import get_city_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/utility/:id_string/service-contract-template/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: ServiceContract Template list
# Usage: API will fetch all Service Contract Template list
# Tables used: UtilityServiceContractTemplate
# Author: Chinmay
# Created on: 27/1/2021

class UtilityServiceContractTemplateList(generics.ListAPIView):
    try:
        serializer_class = UtilityServiceContractTemplateListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityServiceContractTemplateModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(SERVICE_CONTRACT_TEMPLATE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')
