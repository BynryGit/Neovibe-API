import jwt # jwt token library
from api.settings import SECRET_KEY
from v1.userapp.models.user_token import UserToken


def is_token_valid(token):
    return True
    try:
        return UserToken.objects.filter(token=token).exists()
    except:
        return False

def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='RS256')

def get_user(id_string):
    user = User.objects.get(id_string = id_string)
    return user

def is_authorized():
    return True
    privileges = user.privileges.all()
    sub_modules = user.sub_modules.all()
    if privilege in privileges:
        if sub_module in sub_modules:
            return True
    else:
        return False