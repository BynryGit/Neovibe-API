import jwt # jwt token library
from api.settings import SECRET_KEY


def is_token_valid(token):
    return Token.objects.filter(token=token).exists()

def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='RS256')

def get_user(id_string):
    user = User.objects.get(id_string = id_string)
    return user

def is_authorized(user, privilege, sub_module):
    privileges = user.privileges.all()
    sub_modules = user.sub_modules.all()
    if privilege in privileges:
        if sub_module in sub_modules:
            return True
    else:
        return False