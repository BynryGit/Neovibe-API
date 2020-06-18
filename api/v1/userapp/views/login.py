import traceback
import uuid

import jwt

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.messages import *
from api.settings import SECRET_KEY
from master.models import get_user_by_email, get_user_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id
from v1.commonapp.views.logger import logger
from v1.userapp.models.login_trail import LoginTrail
from v1.userapp.models.user_token import UserToken, get_token_by_token, check_token_exists_for_user


def validate_login_data(request):
    if 'email' in request.data and 'password' in request.data:
        return True
    else:
        return False


def set_login_trail(email, status):
    LoginTrail(
        email=email,
        status=status
    ).save()


# def check_form_factor(request, user_obj):
#     if request.data['imei'] != user_obj.imei:
#         return False
#     else:
#         return True


def login(request, user):
    try:
        user_obj = get_user_by_email(user.email)
        form_factor = get_form_factor_by_id(user_obj.form_factor_id)
        payload = {'user_id_string': str(user_obj.id_string), 'string': str(uuid.uuid4().hex[:6].upper())}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        token_obj = UserToken(
            tenant=user_obj.tenant,
            form_factor_id=user_obj.form_factor_id,
            user_id=user_obj.id,
            token=encoded_jwt,
            ip_address=ip,
            created_by=user.id,
            is_active=True
        )
        token_obj.save()
        return token_obj.token
    except Exception as e:
        print(traceback.print_exc())
        logger().log(e, 'ERROR', user='test', name='test')
        return False


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


class LoginApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            if validate_login_data(request):
                email = request.data['email']
                password = request.data['password']

                auth = authenticate(email=email, password=password)

                if auth:
                    token = login(request, auth)  # Call Login function

                    if not token:
                        set_login_trail(email, 'Fail')
                        return Response({
                            STATE: FAIL,
                            RESULTS: INVALID_CREDENTIALS,
                        }, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        set_login_trail(email, 'Success')
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: SUCCESSFUL_LOGIN,
                            Token: token,
                        }, status=status.HTTP_200_OK)
                else:
                    set_login_trail(email, 'Fail')
                    return Response({
                        STATE: FAIL,
                        RESULTS: INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            logger().log(ex, 'ERROR', user='test', name='test')
            return Response({
                STATE: FAIL,
                RESULTS: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/user/logout
# API verb: GET
# Package: Basic
# Modules: User
# Interaction: user list
# Usage: API will fetch required data for user list
# Tables used: 2.5.3. User Details
# Author: Arpita
# Created on: 03/06/2020


def validate_logout_data(request):
    if 'token' in request.headers:
        return True
    else:
        return False


class LogoutApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            if validate_logout_data(request):
                token = request.headers['token']
                user = get_user_by_id_string(request.headers['id-string'])

                if check_token_exists_for_user(token, user.id):
                    token = get_token_by_token(token)
                    token.delete()
                    return Response({
                        STATE: SUCCESS,
                        RESULTS: SUCCESSFUL_LOGOUT,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: FAIL,
                        RESULTS: INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            logger().log(ex, 'ERROR', user='test', name='test')
            return Response({
                STATE: FAIL,
                RESULTS: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

