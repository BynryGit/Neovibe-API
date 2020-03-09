import pdb

import jwt
from django.contrib.auth import authenticate
from rest_framework import serializers
from smart360_API.settings import SECRET_KEY
from userapp.models.user import User, Token

__author__ = "rohan"

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password')

    def login(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user is not None:
            user_obj = User.objects.get(username=user.username)
            if Token.objects.filter(user_id=user_obj).exists():
                token = Token.objects.get(user_id=user_obj)
                token.delete()
            payload = {'id_string': str(user_obj.id_string)}
            encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            token_obj = Token(user_id=user_obj, token=encoded_jwt)
            token_obj.save()
            return token_obj.token
        else:
            return False