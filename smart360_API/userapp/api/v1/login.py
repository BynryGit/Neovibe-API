__author__ = "aki"

import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from smart360_API import messages
from userapp.serializers.login import LoginSerializer


class LoginApiView(APIView):
    """Login Api View"""
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        try:
            if serializer.is_valid():
                token = serializer.login(validated_data = serializer.validated_data)
                if token == False:
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
            else:
                return Response({
                    messages.RESULT: messages.FAIL,
                    messages.MESSAGE: messages.INVALID_CREDENTIALS,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            print('file: {} api {} execption {}'.format('user', 'POST login', str(traceback.print_exc(ex))))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR.format(str(ex)),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
