from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, RESULTS
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.billing.serializers.invoice_bill import *
from v1.commonapp.common_functions import is_authorized, is_token_valid, get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.complaint.models.complaint import *
from v1.complaint.serializers.complaint import *
from v1.consumer.serializers.consumer_scheme_master import *
from v1.payment.serializer.payment import *
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.serializers.meter_status import MeterStatusListSerializer
from v1.commonapp.models.meter_status import MeterStatus as MeterStatusModel
from v1.commonapp.models.region import get_region_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from api.messages import *
from api.constants import *

# API Header
# API end Point: api/v1/:id_string/region/list
# API verb: GET
# Package: Basic
# Modules: Admin
# Sub Module: Admin
# Interaction: regions list
# Usage: API will fetch all region list
# Tables used: Region
# Author: Chinmay
# Created on: 09/11/2020


class MeterStatusList(generics.ListAPIView):
    try:
        serializer_class = MeterStatusListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    # utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = MeterStatusModel.objects.filter(is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Meter Status not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Admin', sub_module='Admin')