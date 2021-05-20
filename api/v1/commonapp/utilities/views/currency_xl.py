import xlrd
from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from v1.commonapp.views.logger import logger
from api.messages import STATE, ERROR, EXCEPTION, SUCCESS, RESULT, METER_NOT_FOUND, SUCCESSFULLY_DATA_SAVE
from api.constants import MX, EDIT, METER_MASTER, VIEW
from master.models import get_user_by_id_string
from v1.commonapp.models.global_lookup import get_global_lookup_by_value
from v1.commonapp.models.lifecycle import LifeCycle as LifeCycleTbl
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.notes import Notes as NoteTbl
from v1.commonapp.models.premises import get_premise_by_name
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.serializers.lifecycle import LifeCycleListSerializer
from v1.commonapp.serializers.note import NoteListSerializer, NoteSerializer, NoteViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.meter_data_management.models.meter_make import get_meter_make_by_name
from v1.meter_data_management.models.route import get_route_by_name
from v1.meter_data_management.views.status import check_meter_status
from v1.userapp.decorators import is_token_validate, role_required
from v1.commonapp.models.currency import Currency as CurrencyTbl
from v1.meter_data_management.serializers.meter import MeterViewSerializer, MeterSerializer
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_name
from v1.commonapp.views.custom_filter_backend import CustomFilter




class CurrencyUpload(GenericAPIView):
    @is_token_validate
    # @role_required(MX, METER_MASTER, EDIT)
    def post(self, request):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                
                currency_values = []
                loc = (r"/home/ubuntu/smart360/api/v1/commonapp/utilities/xls_files/Final Currency.xls")
                workbook = xlrd.open_workbook(loc)
                number_of_rows = workbook.sheets()[0].nrows
                number_of_columns = workbook.sheets()[0].ncols
               

                for row in range(1, number_of_rows):
                    row_values = []
                    for col in range(number_of_columns):
                        value = (workbook.sheets()[0].cell(row, col).value)
                        row_values.append(value)
                    currency_values.append(row_values)

                for value in currency_values:
                    if CurrencyTbl.objects.filter(name=value[0], is_active=True).exists():
                        pass
                    else:
                        CurrencyTbl(
                            name=value[0],
                            key=value[1],
                            is_active=value[2],
                            created_by=value[3],
                            updated_by=value[4]
                        ).save()
                return Response({
                    STATE: SUCCESS,
                    RESULT: SUCCESSFULLY_DATA_SAVE,
                }, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY_MASTER')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
