from rest_framework import status
from rest_framework.response import Response

from v1.commonapp.common_functions import get_payload
from v1.userapp.models.user_token import check_token_exists_for_user
from master.models import get_user_by_id_string
from v1.userapp.models.user_privilege import check_user_privilege_exists
from v1.userapp.models.user_utility import check_user_utility_exists
from v1.commonapp.views.custom_exception import *
from v1.utility.models.utility_master import get_utility_by_id_string


def is_token_validate(function):
    def wrap(request, *args, **kwargs):
        token = args[0].headers['Token']
        decoded_token = get_payload(token)
        if decoded_token:
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if check_token_exists_for_user(token, user_obj.id):
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
            token = args[0].headers['Token']
            decoded_token = get_payload(token)
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if check_user_privilege_exists(user_obj.id, module_id, sub_module_id, privilege_id):
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
        token = args[0].headers['Token']
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
                RESULTS: INVALID_TOKEN,
            }, status=status.HTTP_401_UNAUTHORIZED)
    return wrap








