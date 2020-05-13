import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.campaign.views.common_functions import is_data_verified
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.userapp.models.user_bank_detail import get_bank_by_tenant_id_string
from v1.userapp.models.user_master import get_bank_by_user_id_string
from v1.userapp.serializers.bank_detail import BankListSerializer, BankViewSerializer


# API Header
# API end Point: api/v1/user/bank
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit bank details of users
# Usage: This will display all bank details of user.
# Tables used: 1.3. Tenant - Tenant Bank Details
# Author: Arpita
# Created on: 13/05/2020


class BankList(generics.ListAPIView):
    serializer_class = BankListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        queryset = get_bank_by_tenant_id_string(1)
        utility_id_string = self.request.query_params.get('utility', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        return queryset


# API Header
# API end Point: api/v1/user/bank
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit bank details of users
# Usage: This will display all bank details of user.
# Tables used: 1.3. Tenant - Tenant Bank Details
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

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic role details start
                        user = get_user_by_id_string(request.data['user'])
                        role, result, error = add_basic_role_details(request, user)
                        if result:
                            data = {
                                "role_id_string": role.id_string
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
                        # Save basic role details start
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        user = get_user_by_id_string(request.data['user'])
                        role, result, error = save_edited_basic_role_details(request, user)
                        if result:
                            data = {
                                "role_id_string": role.id_string
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
                        # Save basic details start
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
