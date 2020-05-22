import jwt # jwt token library
from api.settings import SECRET_KEY
# from v1.userapp.models.user_master import UserDetail
# from v1.userapp.models.user_token import UserToken


def is_token_valid(token):
    return True
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_obj = get_user_by_id_string(str(decoded_token))
        if user_obj:
            token_obj = get_token_by_user_id(user_obj.id)
            if token_obj:
                if token_obj.token == token:
                    return True, user_obj.id
                else:
                    return False, ''
            else:
                return False, ''
        else:
            return False, ''
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        raise InvalidAuthorizationException


def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='RS256')


def get_user(id_string):
    return True
    # user = UserDetail.objects.get(id_string = id_string)
    # return user


def is_authorized():
    return True
    # privileges = user.privileges.all()
    sub_modules = user.sub_modules.all()
    if privilege in privileges:
        if sub_module in sub_modules:
            return True
    else:
        return False