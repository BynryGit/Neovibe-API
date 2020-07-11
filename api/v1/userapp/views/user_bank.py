import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.userapp.models.user_bank import get_user_bank_by_user_id, check_user_bank_exists


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
from v1.userapp.serializers.user_bank import UserBankSerializer, UserBankViewSerializer


class UserBankDetail(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            user = get_user_by_id_string(id_string)
            if user:
                user_bank = get_user_bank_by_user_id(user.id)
                if user_bank:
                    serializer = UserBankViewSerializer(instance=user_bank, context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        DATA: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        DATA: BANK_NOT_FOUND,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Bank')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, id_string):
        try:
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                request.data['user_id'] = str(id_string)
                user_bank = check_user_bank_exists(id_string)
                if not user_bank:
                    serializer = UserBankSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=False):
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        user_bank_obj = serializer.create(serializer.validated_data, user)
                        view_serializer = UserBankViewSerializer(instance=user_bank_obj, context={'request': request})
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: view_serializer.data,
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: list(serializer.errors.values())[0][0],
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    raise CustomAPIException(BANK_ALREADY_EXISTS, status_code=status.HTTP_404_NOT_FOUND)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Bank')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            # TODO for testing.py start
            # if not request.data._mutable:
            #     request.data._mutable = True
            # TODO for testing.py end
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                request.data['user_id'] = str(id_string)
                user_bank = get_user_bank_by_user_id(user_obj.id)
                if user_bank:
                    serializer = UserBankSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=False):
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        user_bank_obj = serializer.update(user_bank, serializer.validated_data, user)
                        view_serializer = UserBankViewSerializer(instance=user_bank_obj, context={'request': request})
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
                    raise CustomAPIException(BANK_NOT_FOUND_FOR_USER, status_code=status.HTTP_404_NOT_FOUND)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module='Admin', sub_module='User Bank')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


