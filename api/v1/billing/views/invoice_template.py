
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from v1.billing.models.bill import get_bill_by_id_string
from v1.billing.models.bill import get_bill_by_id_string
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.billing.models.invoice_template import get_rendering_invoice_template_by_utility_id_string
from api.messages import *
from api.constants import *
import traceback
import rest_framework
from rest_framework import status, generics
from v1.billing.views.common_functions import generate_formate,html_handler
from v1.billing.models.bill import get_bill_by_schedule_log_consumer_no
from v1.billing.models.bill_schedule_log import get_schedule_bill_log_by_id_string
# API Header
# API end Point: api/v1/invoice-template/
# API verb: GET
# Package: Basic
# Modules: Bill
# Sub Module: Bill
# Interaction: Generate Invoice
# Usage: View, Edit User
# Tables used: Invoice Template
# Author: Priyanka
# Created on: 10/04/2021

import html
from bs4 import BeautifulSoup
from django.http import HttpResponse

class InvoiceTemplate(GenericAPIView):

    @is_token_validate
    # role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get(self, request,consumer_no,schedule_log_id_string):
        try:
            print('====schedule_log_id_string====',schedule_log_id_string)
            print('=======consumer_no============',consumer_no)
            schedule_id = get_schedule_bill_log_by_id_string(schedule_log_id_string)
            print('=====schedule_id=====',schedule_id)
            if schedule_id:
                bill_obj = get_bill_by_schedule_log_consumer_no(consumer_no,schedule_id.id)
                print('------bill_obj-------',bill_obj)
                if bill_obj:
                    return Response({
                        STATE: SUCCESS,
                        RESULT: bill_obj.invoice_template,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        RESULTS: ID_STRING_NOT_FOUND,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    STATE: EXCEPTION,
                    RESULTS: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('===Exception===',e)
            # logger().log(e, 'MEDIUM', module='Admin', sub_module='User')
            return Response({
                STATE: EXCEPTION,
                RESULTS: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
