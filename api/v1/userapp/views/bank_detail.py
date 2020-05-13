import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_bank_detail import get_bank_by_tenant_id_string, get_bank_by_utility_id_string
from v1.userapp.models.user_master import get_bank_by_user_id_string
from v1.userapp.serializers.bank_detail import BankListSerializer, BankViewSerializer


# API Header
# API end Point: api/v1/user/bank/list
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View bank list
# Usage: This will display list of bank.
# Tables used: User - User Bank Details
# Author: Arpita
# Created on: 13/05/2020


class BankList(generics.ListAPIView):
    serializer_class = BankListSerializer

    def get_queryset(self):

        queryset = get_bank_by_tenant_id_string(1)
        utility_id_string = self.request.query_params.get('utility', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        return queryset


# API Header
# API end Point: api/v1/user/bank
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View bank list
# Usage: This will display list of bank.
# Tables used: User - User Bank Details
# Author: Arpita
# Created on: 13/05/2020


class GetBankList(generics.ListAPIView):
    serializer_class = BankListSerializer

    def get_queryset(self):

        queryset = get_bank_by_utility_id_string(1)
        return queryset


# API Header
# API end Point: api/v1/user/bank
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit bank details of users
# Usage: This will display all bank details of user.
# Tables used: User - User Bank Details
# Author: Arpita
# Created on: 13/05/2020

class Bank(GenericAPIView):

    def get(self, request, id_string):
        try:
            bank = get_bank_by_user_id_string(id_string)
            if bank:
                serializer = BankViewSerializer(instance=bank, context={'request': request})
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

