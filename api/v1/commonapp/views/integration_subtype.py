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
from v1.commonapp.serializers.integration_subtype import IntegrationSubTypeListSerializer
from v1.commonapp.models.integration_subtype import IntegrationSubType as IntegrationSubTypeModel
from v1.utility.models.utility_master import get_utility_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/:id_string/integration_subtype/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Integration SubType list
# Usage: API will fetch all Integration SUbType list
# Tables used: Integration SubType
# Author: Chinmay
# Created on: 19/11/2020

class IntegrationSubTypeList(generics.ListAPIView):
    try:
        serializer_class = IntegrationSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = IntegrationSubTypeModel.objects.filter(is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Integration Sub Type not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')
