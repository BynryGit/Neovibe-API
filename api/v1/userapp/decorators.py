from django.core.exceptions import PermissionDenied
from v1.commonapp.common_functions import get_payload
from v1.userapp.models.user_token import check_token_exists_for_user
from master.models import get_user_by_id_string
from v1.userapp.models.user_privilege import check_user_privilege_exists


def is_token_validate(function):
    def wrap(request, *args, **kwargs):
        token = args[0].headers['Token']
        decoded_token = get_payload(token)
        if decoded_token:
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if check_token_exists_for_user(token, user_obj.id):
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    return wrap


def role_required(user_id, module_id, sub_module_id, privilege_id):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if check_user_privilege_exists(user_id, module_id, sub_module_id, privilege_id):
                return view_method(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _arguments_wrapper
    return _method_wrapper







