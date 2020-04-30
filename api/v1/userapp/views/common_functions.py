import jwt
from django.contrib.auth import authenticate
from api.settings import SECRET_KEY
from v1.userapp.models.user_master import SystemUser
from v1.userapp.models.user_token import UserToken


def login(validated_data):
    user = authenticate(username=validated_data['username'], password=validated_data['password'])
    if user is not None:
        user_obj = SystemUser.objects.get(username=user.username)
        if UserToken.objects.filter(user_id=user_obj).exists():
            token = UserToken.objects.get(user_id=user_obj)
            token.delete()
        payload = {'id_string': str(user_obj.id_string)}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token_obj = UserToken(user_id=user_obj, token=encoded_jwt)
        token_obj.save()
        return token_obj.token
    else:
        return False
