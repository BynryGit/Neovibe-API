from rest_framework import status, generics
from api.messages import *
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.service.models.consumer_services import get_consumer_services_by_consumer_no
from v1.service.serializers.service import ServiceDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.serializers.utility_document_type import UtilityDocumentTypeListSerializer
from v1.utility.models.utility_document_type import UtilityDocumentType as UtilityDocumentTypeModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.region import get_region_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/utility/:id_string/document_type/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: Utility Document Type list
# Usage: API will fetch all Document Type list
# Tables used: UtilityDocumentType
# Author: Chinmay
# Created on: 22/1/2020

class UtilityDocumentTypeList(generics.ListAPIView):
    try:
        serializer_class = UtilityDocumentTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityDocumentTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(DOCUMENT_TYPE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')
