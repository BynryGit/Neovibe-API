import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api import messages
from v1.userapp.views.common_functions import login

# API Header
# API end Point: api/v1/user/login
# API verb: GET
# Package: Basic
# Modules: User
# Interaction: user list
# Usage: API will fetch required data for user list
# Tables used: 2.5.3. User Details
# Author: Arpita
# Created on: 29/04/2020


class LoginApiView(APIView):
    """Login Api View"""
    def post(self, request, format=None):
        try:
            validated_data = {
                'username': request.data['username'],
                'password': request.data['password']
            }

            token = login(validated_data = validated_data) # Call Login function

            if not token:
                return Response({
                    messages.RESULT: messages.FAIL,
                    messages.MESSAGE: messages.INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    messages.RESULT: messages.SUCCESS,
                    messages.MESSAGE: messages.SUCCESSFULLY_DATA_RETRIEVE,
                    messages.Token: token,
                }, status=status.HTTP_200_OK)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginApiView(APIView):
    """Login Api View"""
    def post(self, request, format=None):
        try:
            validated_data = {
                'username': request.data['username'],
                'password': request.data['password']
            }

            token = login(validated_data = validated_data) # Call Login function

            if not token:
                return Response({
                    messages.RESULT: messages.FAIL,
                    messages.MESSAGE: messages.INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    messages.RESULT: messages.SUCCESS,
                    messages.MESSAGE: messages.SUCCESSFULLY_DATA_RETRIEVE,
                    messages.Token: token,
                }, status=status.HTTP_200_OK)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
