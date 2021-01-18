from rest_framework import status, generics
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
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
from v1.service.models.consumer_service_details import get_consumer_services_by_consumer_no
from v1.service.serializers.service import ServiceDetailListSerializer
from v1.userapp.decorators import is_token_validate, role_required
from v1.utility.serializers.utility_department_subtype import UtilityDepartmentSubTypeListSerializer
from v1.utility.models.utility_department_subtype import UtilityDepartmentSubType as UtilityDepartmentSubTypeModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.models.region import get_region_by_id_string
from api.messages import *
from api.constants import *


# API Header
# API end Point: api/v1/:id_string/dept_subtype/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: regions list
# Usage: API will fetch all region list
# Tables used: Region
# Author: Chinmay
# Created on: 19/11/2020

class UtilityDepartmentSubTypeList(generics.ListAPIView):
    try:
        serializer_class = UtilityDepartmentSubTypeListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = UtilityDepartmentSubTypeModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Department Subtype not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')