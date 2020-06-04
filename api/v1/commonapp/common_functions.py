import jwt # jwt token library
from api.settings import SECRET_KEY
from master.models import get_user_by_id_string, check_user_id_string_exists
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_privilege import check_user_privilege_exists
from v1.userapp.models.user_token import check_token_exists
from v1.userapp.models.user_utility import check_user_utility_exists


def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


def is_token_valid(token):
    try:
        if check_token_exists(token):
            decoded_token = get_payload(token)
            user_obj = get_user_by_id_string(decoded_token['user_id_string'])
            if user_obj:
                return True, user_obj
            else:
                return False
        else:
            return False
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


def get_user(id_string):
    return True
    # user = UserDetail.objects.get(id_string = id_string)
    # return user


def is_authorized(module_id, sub_module_id, privilege_id, user_obj):
    try:
        if check_user_id_string_exists(user_obj.id_string):
            if check_user_privilege_exists(user_obj.id, module_id, sub_module_id, privilege_id):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


def is_utility(utility_id, user_obj):
    try:
        if check_user_id_string_exists(user_obj.id_string):
            if check_user_utility_exists(user_obj.id, utility_id):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False
