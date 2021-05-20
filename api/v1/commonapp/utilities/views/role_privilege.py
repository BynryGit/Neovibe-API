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
from v1.commonapp.common_functions import is_token_valid, is_authorized, get_user_from_token
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from v1.userapp.decorators import is_token_validate, role_required
from v1.userapp.models.role_privilege import RolePrivilege as RolePrivilegeTbl
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_name
from v1.commonapp.views.custom_filter_backend import CustomFilter
from v1.tenant.models.tenant_master import get_tenant_by_id_string





class RolePrivilegeUpload(GenericAPIView):
    @is_token_validate
    # @role_required(MX, METER_MASTER, EDIT)
    def post(self, request, id_string):
        try:
            with transaction.atomic():
                user_id_string = get_user_from_token(request.headers['Authorization'])
                tenant_obj = get_tenant_by_id_string(id_string)
                role_privilege_values = []
                loc = (r"/home/ubuntu/smart360/api/v1/commonapp/utilities/xls_files/Role-Privilege-Final.xls")
                workbook = xlrd.open_workbook(loc)
                number_of_rows = workbook.sheets()[0].nrows
                number_of_columns = workbook.sheets()[0].ncols
               

                for row in range(1, number_of_rows):
                    row_values = []
                    for col in range(number_of_columns):
                        value = (workbook.sheets()[0].cell(row, col).value)
                        row_values.append(value)
                    role_privilege_values.append(row_values)

                for value in role_privilege_values:
                    if RolePrivilegeTbl.objects.filter(tenant=tenant_obj,role_id=value[1],module_id=value[2],sub_module_id=value[3],privilege_id=value[4], is_active=True).exists():
                        pass
                    else:
                        RolePrivilegeTbl(
                            tenant=tenant_obj,
                            role_id=value[1],
                            module_id=value[2],
                            sub_module_id=value[3],
                            privilege_id=value[4],
                            is_active = value[5]
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