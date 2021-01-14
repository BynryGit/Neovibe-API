from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no, get_invoice_bill_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.meter_data_management.serializers.read_cycle import ReadCycleViewSerializer, ReadCycleSerializer, ReadCycleListSerializer
from v1.meter_data_management.models.read_cycle import ReadCycle as ReadCycleModel
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id_string
from api.messages import READ_CYCLE_NOT_FOUND, SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from api.constants import *

# API Header
# API end Point: api/v1/utility/:id_string/read_cycle/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: ReadCycle list
# Usage: API will fetch all Read Cycle list
# Tables used: ReadCycle
# Author: Chinmay
# Created on: 12/1/2021


class ReadCycleList(generics.ListAPIView):
    try:
        serializer_class = ReadCycleListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = ReadCycleModel.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException(READ_CYCLE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Utility')