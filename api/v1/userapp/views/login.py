import traceback
import jwt
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.messages import *
from api.settings import SECRET_KEY
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_master import get_user_by_username
from v1.userapp.models.user_token import UserToken, get_token_by_user_id


# API Header
# API end Point: api/v1/user/login
# API verb: GET
# Package: Basic
# Modules: User
# Interaction: user list
# Usage: API will fetch required data for user list
# Tables used: 2.5.3. User Details
# Author: Arpita
# Created on: 23/05/2020

def login(request, user):
    try:
        user_obj = get_user_by_username(user.username)
        token_obj = get_token_by_user_id(user_obj.id)
        if request.data['imei']:
            if request.data['imei'] != user_obj.imei:
                return False
        if token_obj:
            token_obj.delete()
        payload = {'id_string': str(user_obj.id_string)}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        token_obj = UserToken(
            tenant=user_obj.tenant,
            utility=user_obj.utility,
            form_factor=user_obj.form_factor_id,
            user_id=user_obj.id,
            token=encoded_jwt,
            ip_address = ip,
            created_by=user.id,
            is_active = True
        )
        token_obj.save()
        return token_obj.token
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


class LoginApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
            imei = request.data['imei']

            if imei:
                auth = is_imei_valid()
            else:
                auth = authenticate(username=username, password=password)

            if auth:
                token = login(request, auth)  # Call Login function

                if not token:
                    return Response({
                        STATE: FAIL,
                        RESULTS: INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: SUCCESSFULLY_DATA_RETRIEVE,
                        Token: token,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: FAIL,
                    RESULTS: INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            logger().log(ex, 'ERROR', user='test', name='test')
            return Response({
                STATE: FAIL,
                RESULTS: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
