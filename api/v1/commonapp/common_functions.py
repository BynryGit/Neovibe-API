import jwt # jwt token library
from api.settings import SECRET_KEY
from v1.commonapp.views.custom_exception import InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.userapp.models.role_privilege import get_record_by_values, get_record_values_by_id
from v1.userapp.models.user_master import get_user_by_id_string
from v1.userapp.models.user_role import get_user_role_by_user_id
from v1.userapp.models.user_token import get_token_by_user_id


def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


def is_token_valid(token):
    # return True
    try:
        decoded_token = get_payload(token)
        print('==============',decoded_token)
        user_obj = get_user_by_id_string(str(decoded_token['id_string']))
        if user_obj:
            token_obj = get_token_by_user_id(user_obj.id)
            if token_obj:
                if token_obj.token == token:
                    return True
                else:
                    return False
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


def is_authorized():
    return True


# def is_authorized(module_id, sub_module_id, privilege_id, token):
#     try:
#         data = False
#         decoded_token = get_payload(token)
#         user_obj = get_user_by_id_string(str(decoded_token['id_string']))
#         roles = get_user_role_by_user_id(user_obj.id)
#         if roles:
#             for role in roles:
#                 privilege = get_record_values_by_id(role.id,module_id,sub_module_id,privilege_id)
#                 if privilege:
#                     data = True
#                     return data
#                 else:
#                     data = False
#             return data
#         else:
#             return data
#     except Exception as e:
#         logger().log(e, 'ERROR', user='test', name='test')
#         return False
