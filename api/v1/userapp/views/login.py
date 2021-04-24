import traceback
import uuid
import jwt
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.messages import *
from master.models import get_user_by_email, get_user_by_id_string, get_all_users
from v1.commonapp.views.logger import logger
from v1.commonapp.views.secret_reader import SecretReader
from v1.userapp.models.login_trail import LoginTrail
from v1.userapp.models.user_token import UserToken, get_token_by_token, check_token_exists_for_user
from v1.consumer.models.consumer_master import get_consumer_by_email
from v1.consumer.models.consumer_token import ConsumerToken
from v1.commonapp.common_functions import get_payload
from v1.consumer.models.consumer_master import get_consumer_by_id_string
# from v1.tenant.models.tenant_master import get_tenant_by_short_name
from v1.consumer.models.consumer_master import ConsumerMaster
from v1.consumer.models.consumer_token import get_consumer_token_by_token,check_token_exists_for_consumer
from v1.commonapp.views.settings_reader import SettingReader
secret_reader = SecretReader()
setting_reader = SettingReader()


# def validate_login_data(request):
#     if 'email' in request.data and 'password' in request.data:
#         return True
#     else:
#         return False

def validate_login_data(request):
    if 'username' in request.data and 'password' in request.data:
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


# def login(request, user):
#     try:
#         user_obj = get_user_by_email(user.email)
#         payload = {'user_id_string': str(user_obj.id_string), 'string': str(uuid.uuid4().hex[:6].upper())}
#         encoded_jwt = jwt.encode(payload, secret_reader.get_secret(), algorithm='HS256').decode('utf-8')
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         token_obj = UserToken(
#             tenant=user_obj.tenant,
#             form_factor_id=user_obj.form_factor_id,
#             user_id=user_obj.id,
#             token=encoded_jwt,
#             ip_address=ip,
#             created_by=user.id,
#             created_date = datetime.utcnow(),
#             is_active=True
#         )
#         token_obj.save()
#         return token_obj.token
#     except Exception as e:
#         print("############",e)
#         print(traceback.print_exc())
#         logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Login')
#         return False

# form factor 1 ==> user web
# form factor 2 ==>  user mobile
# form factor 3 ==>  consumer web
# form factor 4 ==> consumer mobile

def login(request, user, form_factor):
    try:
        if (form_factor == 1 or form_factor == 2):
            user_obj = get_user_by_email(user.email)
            payload = {'user_id_string': str(user_obj.id_string),'type':setting_reader.get_user(), 'string': str(uuid.uuid4().hex[:6].upper())}
            print("=======PAYLOAD======",payload)
            encoded_jwt = jwt.encode(payload, secret_reader.get_secret(), algorithm='HS256').decode('utf-8')
            print("=======ENCODED TOKEN==========",encoded_jwt)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
                print(user_obj.id, encoded_jwt, ip, user.id, datetime.utcnow())
            token_obj = UserToken(
                tenant=user_obj.tenant,
                # form_factor_id=user_obj.form_factor_id,
                user_id=user_obj.id,
                token=encoded_jwt,
                ip_address=ip,
                created_by=user.id,
                created_date = datetime.utcnow(),
                is_active=True
            )
            token_obj.save()
            return token_obj.token

        elif(form_factor == 3 or form_factor == 4):
            print("111111111111111",request.data['tenant'])
            print("user",user)
            tenant_obj = get_tenant_by_short_name(request.data['tenant'])
            print("this is tenant=======",tenant_obj)
            c_obj = ConsumerMaster.objects.get(email=user.email, tenant=tenant_obj)
            print("=======consumer master=====",c_obj.id_string)
            consumer_obj = get_consumer_by_email(user.email)
            payload = {'user_id_string': str(consumer_obj.id_string), 'type':setting_reader.get_consumer_user(),'string': str(uuid.uuid4().hex[:6].upper())}
            print("=======PAYLOAD======",payload)
            encoded_jwt = jwt.encode(payload, secret_reader.get_secret(), algorithm='HS256').decode('utf-8')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            token_obj = ConsumerToken(
                tenant=consumer_obj.tenant,
                # form_factor_id=consumer_obj.form_factor_id,
                consumer_id=consumer_obj.id,
                token=encoded_jwt,
                ip_address=ip,
                created_by=user.id,
                created_date = datetime.utcnow(),
                is_active=True
            )
            token_obj.save()
            return token_obj.token
    except Exception as e:
        print("===error===",e)
        print(traceback.print_exc())
        logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Login')
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


# class LoginApiView(APIView):
#     """Login Api View"""

#     def post(self, request, format=None):
#         try:
#             if validate_login_data(request):
#                 email = request.data['email']
#                 password = request.data['password']

#                 auth = authenticate(email=email, password=password)

#                 if auth:
#                     token = login(request, auth)  # Call Login function

#                     if not token:
#                         set_login_trail(email, 'Fail')
#                         return Response({
#                             STATE: FAIL,
#                             RESULTS: INVALID_CREDENTIALS,
#                         }, status=status.HTTP_401_UNAUTHORIZED)
#                     else:
#                         set_login_trail(email, 'Success')
#                         user = get_user_by_email(email)
#                         return Response({
#                             STATE: SUCCESS,
#                             RESULTS: SUCCESSFUL_LOGIN,
#                             Token: token,
#                             ID_STRING: user.id_string,
#                             EMAIL:user.email,
#                             ID : user.id


#                         }, status=status.HTTP_200_OK)
#                 else:
#                     set_login_trail(email, 'Fail')
#                     return Response({
#                         STATE: FAIL,
#                         RESULTS: INVALID_CREDENTIALS,
#                     }, status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as ex:
#             print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
#             logger().log(ex, 'HIGH', module = 'Admin', sub_module = 'User Login')
#             return Response({
#                 STATE: FAIL,
#                 RESULTS: SERVER_ERROR.format(str(ex)),
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            if validate_login_data(request):
                username = request.data['username']
                password = request.data['password']
                form_factor = request.data['form_factor']
                auth = authenticate(username=username, password=password, form_factor=form_factor)
                if auth:
                    token = login(request, auth, form_factor)  # Call Login function

                    if not token:
                        set_login_trail(username, 'Fail')
                        return Response({
                            STATE: FAIL,
                            RESULTS: INVALID_CREDENTIALS,
                        }, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        set_login_trail(username, 'Success')
                        if (form_factor == 1 or form_factor == 2):
                            user = get_user_by_email(auth.email)
                        elif (form_factor == 3 or form_factor == 4):
                            user = get_consumer_by_email(auth.email)
                        return Response({
                            STATE: SUCCESS,
                            RESULTS: SUCCESSFUL_LOGIN,
                            Token: token,
                            ID_STRING: user.id_string
                        }, status=status.HTTP_200_OK)
                else:
                    set_login_trail(username, 'Fail')
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
            logger().log(ex, 'HIGH', module = 'Admin', sub_module = 'User Login')
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
    if 'Authorization' in request.headers:
        return True
    else:
        return False


# class LogoutApiView(APIView):
#     """Login Api View"""

#     def post(self, request, format=None):
#         try:
#             if validate_logout_data(request):
#                 token = request.headers['Authorization']
#                 print("=========this is token---------",token)
#                 user = get_user_by_id_string(request.data['id_string'])

#                 if check_token_exists_for_user(token, user.id):
#                     token = get_token_by_token(token)
#                     token.delete()
#                     return Response({
#                         STATE: SUCCESS,
#                         RESULTS: SUCCESSFUL_LOGOUT,
#                     }, status=status.HTTP_200_OK)
#                 else:
#                     return Response({
#                         STATE: FAIL,
#                         RESULTS: INVALID_CREDENTIALS,
#                     }, status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as ex:
#             print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
#             logger().log(ex, 'HIGH', module = 'Admin', sub_module = 'User Logout')
#             return Response({
#                 STATE: FAIL,
#                 RESULTS: SERVER_ERROR.format(str(ex)),
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutApiView(APIView):
    """Login Api View"""

    def post(self, request, format=None):
        try:
            if validate_logout_data(request):
                token = request.headers['Authorization']
                decoded_token = get_payload(token)
                print("=========this is token---------",decoded_token)
                if decoded_token:
                    if decoded_token['type'] == setting_reader.get_user():
                        user_obj = get_user_by_id_string(request.data['id_string'])
                        if check_token_exists_for_user(token, user_obj.id):
                            token_obj = get_token_by_token(token)
                            token_obj.delete()
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: SUCCESSFUL_LOGOUT,
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                STATE: FAIL,
                                RESULTS: INVALID_CREDENTIALS,
                            }, status=status.HTTP_401_UNAUTHORIZED)

                    elif decoded_token['type'] == setting_reader.get_consumer_user():
                        consumer_obj = get_consumer_by_id_string(request.data['id_string'])
                        print("------USER--------",consumer_obj)
                        if check_token_exists_for_consumer(token, consumer_obj.id):
                            token_obj = get_consumer_token_by_token(token)
                            token_obj.delete()
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
                        RESULTS: INVALID_TOKEN,
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            logger().log(ex, 'HIGH', module = 'Admin', sub_module = 'User Logout')
            return Response({
                STATE: FAIL,
                RESULTS: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

