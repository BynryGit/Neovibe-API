__author__ = "aki"

import jwt
from django.contrib.auth import authenticate
from rest_framework .views import APIView
from rest_framework.response import Response
from rest_framework import status
from smart360_API import messages
from smart360_API.settings import SECRET_KEY
from userapp.models.user import User, Token


class LoginApiView(APIView):
    """Login Api View"""
    def post(self, request, format=None):
        try:
            print(request.data)
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user:
                user_obj = User.objects.get(username=user.username)

                if Token.objects.filter(user_id=user_obj).exists():
                    token = Token.objects.get(user_id=user_obj)
                    token.delete()

                payload = {'id_string': str(user_obj.id_string)}
                encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
                token_obj = Token(user_id = user_obj, token = encoded_jwt)
                token_obj.save()
                return Response({
                    messages.RESULT: messages.SUCCESS,
                    messages.MESSAGE: messages.SUCCESSFULLY_DATA_RETRIEVE,
                    messages.Token: token_obj.token,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    messages.RESULT: messages.FAIL,
                    messages.MESSAGE: messages.INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(ex)))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
