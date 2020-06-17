import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.tenant.models.tenant_bank_details import get_tenant_bank_details_by_id
from v1.tenant.serializers.tenant_bank_detail import TenantBankDetailSerializer
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.userapp.models.user_bank import get_user_bank_by_user_id
from v1.userapp.serializers.user import UserViewSerializer, UserSerializer


# API Header
# API end Point: api/v1/user/:id_string/bank
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit user bank detail
# Usage: View, Add, Edit User bank detail
# Tables used: 2.5 Users & Privileges - User Bank Details
# Author: Arpita
# Created on: 21/05/2020


class UserBankDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            user_bank = get_user_bank_by_user_id(user.id)
            if user_bank:
                bank = get_tenant_bank_details_by_id(user_bank.bank_id)
                serializer = TenantBankDetailSerializer(instance=bank, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                raise CustomAPIException("Bank detail not found.", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def post(self, request, id_string):
        try:
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    user_obj = serializer.update(user_obj, serializer.validated_data, user)
                    view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise CustomAPIException("Bank detail not found.", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def put(self, request, id_string):
        try:
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    user_id_string = get_user_from_token(request.headers['token'])
                    user = get_user_by_id_string(user_id_string)
                    user_obj = serializer.update(user_obj, serializer.validated_data, user)
                    view_serializer = UserViewSerializer(instance=user_obj, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: view_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: list(serializer.errors.values())[0][0],
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


