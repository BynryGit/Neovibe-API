import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_bank_detail import get_bank_by_tenant_id_string, get_bank_by_utility_id_string
from v1.userapp.models.user_master import get_bank_by_user_id_string, get_user_by_id_string, get_user_by_id
from v1.userapp.serializers.bank_detail import BankListSerializer, UserBankViewSerializer, UserBankSerializer
from v1.userapp.views.common_functions import is_bank_data_verified


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
                serializer = UserBankViewSerializer(instance=bank, context={'request': request})
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

    def post(self, request, format=None):
        try:
            if is_token_valid(self.request.headers['token']):
                if is_authorized():
                    if is_bank_data_verified(request):
                        user = get_user_by_id(3)
                        serializer = UserBankSerializer(data=request.data)
                        if serializer.is_valid():
                            bank_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = UserBankViewSerializer(instance=bank_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Request data verification start
            if is_bank_data_verified(request):
                # Request data verification end

                # Save privilege details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = save_edited_bank_details(request, user)
                if result:
                    data = {
                        "user_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Save privilege details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

