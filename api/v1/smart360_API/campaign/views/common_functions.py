import jwt

from api.v1.smart360_API.smart360_API.settings import SECRET_KEY


def is_token_valid(token):
    return Token.objects.filter(token=token).exists()

def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='RS256')

def get_user(id_string):
    user = User.objects.get(id_string = id_string)
    return user

def check_authorization(user, privillege, sub_module):
    privilleges = user.privilleges.all()
    sub_modules = user.sub_modules.all()
    if privillege in privilleges:
        if sub_module in sub_modules:
            return True
    else:
        return False