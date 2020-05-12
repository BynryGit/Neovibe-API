import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.messages import *
from v1.userapp.views.common_functions import login, authentication

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

            auth = authentication(validated_data)

            if auth:
                token = login(auth) # Call Login function

                if not token:
                    return Response({
                        RESULT: FAIL,
                        MESSAGE: INVALID_CREDENTIALS,
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        RESULT: SUCCESS,
                        MESSAGE: SUCCESSFULLY_DATA_RETRIEVE,
                        Token: token,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    RESULT: FAIL,
                    MESSAGE: INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            return Response({
                RESULT: FAIL,
                MESSAGE: SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)