from v1.commonapp.common_functions import get_payload
from v1.userapp.models.user_token import check_token_exists_for_user
from master.models import get_user_by_id_string
from v1.userapp.models.user_privilege import check_user_privilege_exists
from v1.userapp.models.user_utility import check_user_utility_exists
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import *


def is_token_validate(function):
    def wrap(request, *args, **kwargs):
        token = args[0].headers['Token']
        decoded_token = get_payload(token)
        if decoded_token:
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if check_token_exists_for_user(token, user_obj.id):
                return function(request, *args, **kwargs)
            else:
                raise InvalidTokenException
        else:
            raise InvalidTokenException
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
                raise InvalidAuthorizationException
        return _arguments_wrapper
    return _method_wrapper


def utility_required(utility_id):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            token = args[0].headers['Token']
            decoded_token = get_payload(token)
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if check_user_utility_exists(user_obj.id, utility_id):
                return view_method(request, *args, **kwargs)
            else:
                raise InvalidAuthorizationException
        return _arguments_wrapper
    return _method_wrapper







