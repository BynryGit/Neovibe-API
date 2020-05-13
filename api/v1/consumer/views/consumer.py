import traceback
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import STATE, DATA, ERROR, EXCEPTION, SUCCESS
from v1.billing.models.invoice_bill import get_invoice_bills_by_consumer_no
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.serializers.consumer import ConsumerViewSerializer, ConsumerBillListSerializer


# API Header
# API end Point: api/v1/consumer/bills
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Consumer bill list
# Usage: API will fetch required data for Registration list
# Tables used: Billing - InvoiceBill
# Author: Rohan
# Created on: 12/05/2020
class ConsumerBills(generics.ListAPIView):
    serializer_class = ConsumerBillListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        consumer_id_string = self.request.query_params.get('consumer_id_string', None)
        queryset = get_invoice_bills_by_consumer_no(consumer_id_string)
        return queryset


# API Header
# API end Point: api/v1/consumer/id_string
# API verb: GET
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Consumer details
# Usage: API will fetch required data for Registration list
# Tables used: Consumer - ConsumeMaster
# Author: Rohan
# Created on: 12/05/2020
class Consumer(GenericAPIView):

    def get(self, request, id_string):
        try:
            consumer = get_consumer_by_id_string(id_string)
            if consumer:
                serializer = ConsumerViewSerializer(instance=consumer, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

