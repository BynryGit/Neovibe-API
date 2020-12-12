from datetime import datetime, timedelta, timezone

from rest_framework import status
from rest_framework.response import Response

from v1.commonapp.common_functions import get_payload
from v1.userapp.models.role_privilege import check_role_privilege_exists
from v1.userapp.models.user_role import get_user_role_by_user_id
from v1.userapp.models.user_token import check_token_exists_for_user, get_token_by_token
from master.models import get_user_by_id_string
from v1.userapp.models.user_utility import check_user_utility_exists
from v1.commonapp.views.custom_exception import *
from v1.utility.models.utility_master import get_utility_by_id_string
from rest_framework import permissions


def is_token_validate(function):
    def wrap(request, *args, **kwargs):
        token = args[0].headers['Authorization']
        decoded_token = get_payload(token)
        if decoded_token:
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if check_token_exists_for_user(token, user_obj.id):
                token_obj = get_token_by_token(token)
                if (token_obj.created_date + timedelta(hours=4)).replace(tzinfo=None) < datetime.now():
                # if (token_obj.created_date + timedelta(minutes=1)).replace(tzinfo=None) < datetime.now():
                    token_obj.delete()
                    return Response({
                        STATE: ERROR,
                        RESULTS: TOKEN_EXPIRED,
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return function(request, *args, **kwargs)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: INVALID_TOKEN,
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                STATE: ERROR,
                RESULTS: INVALID_TOKEN,
            }, status=status.HTTP_401_UNAUTHORIZED)
    return wrap


def role_required(module_id, sub_module_id, privilege_id):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            token = args[0].headers['Authorization']
            decoded_token = get_payload(token)
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            roles = get_user_role_by_user_id(user_obj.id)
            if check_role_privilege_exists(roles, module_id, sub_module_id, privilege_id):
                return view_method(request, *args, **kwargs)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: UNAUTHORIZED_USER,
                }, status=status.HTTP_403_FORBIDDEN)
        return _arguments_wrapper
    return _method_wrapper


def utility_required(function):
    def wrap(request, *args, **kwargs):
        token = args[0].headers['Authorization']
        if 'utility_id' in args[0].data:
            utility = args[0].data['utility_id']
            decoded_token = get_payload(token)
            if decoded_token:
                user_obj = get_user_by_id_string(decoded_token['user_id_string'])
                utility = get_utility_by_id_string(utility)
                if check_user_utility_exists(user_obj.id,utility.id ):
                    return function(request, *args, **kwargs)
                else:
                    return Response({
                        STATE: ERROR,
                        RESULTS: UNAUTHORIZED_UTILITY,
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: UNAUTHORIZED_UTILITY,
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                STATE: ERROR,
                RESULTS: UTILITY_NOT_FOUND,
            }, status=status.HTTP_401_UNAUTHORIZED)
    return wrap








