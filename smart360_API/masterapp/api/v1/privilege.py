__author__ = "Arpita"

import traceback
from rest_framework.views import APIView
from masterapp.models.privilege import Privilege
from masterapp.serializers.privilege import PrivilegeSerializer, CreatePrivilegeSerializer
from rest_framework.response import Response
from smart360_API import messages
from rest_framework import status


class PrivilegeApiView(APIView):
    """Privilege Api View"""
    def get(self, request, format=None):
        print(request.data)
        try:
            privilege = Privilege.objects.filter(is_deleted=False)
            serializer = PrivilegeSerializer(privilege,many=True)
            return Response({
                messages.RESULT: messages.SUCCESS,
                messages.MESSAGE: messages.SUCCESSFULLY_DATA_RETRIEVE,
                messages.RESPONSE_DATA : serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as ex:
            print('Exception',traceback.print_exc(ex))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        print(request.data)
        try:
            serializer = CreatePrivilegeSerializer(data=request.data)
            if serializer.is_valid():
                create = serializer.create(serializer.validated_data,request.headers['Token'])
                if create:
                    return Response({
                        messages.RESULT: messages.SUCCESS,
                        messages.MESSAGE: messages.SUCCESSFULLY_DATA_SAVE,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        messages.RESULT: messages.FAIL,
                        messages.MESSAGE: messages.DATA_ALREADY_EXISTS,
                    }, status=status.HTTP_200_OK)
        except Exception as ex:
            print('Exception',traceback.print_exc(ex))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        print(request.data)
        try:
            serializer = CreatePrivilegeSerializer(data=request.data)
            if serializer.is_valid():
                update = serializer.update(serializer.validated_data,request.headers['Token'])
                if update:
                    return Response({
                        messages.RESULT: messages.SUCCESS,
                        messages.MESSAGE: messages.SUCCESSFULLY_DATA_UPDATED,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        messages.RESULT: messages.FAIL,
                        messages.MESSAGE: messages.DATA_NOT_EXISTS,
                    }, status=status.HTTP_200_OK)
        except Exception as ex:
            print('Exception',traceback.print_exc(ex))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        print(request.data)
        try:
            serializer = CreatePrivilegeSerializer(data=request.data)
            if serializer.is_valid():
                delete = serializer.delete(serializer.validated_data)
                if delete:
                    return Response({
                        messages.RESULT: messages.SUCCESS,
                        messages.MESSAGE: messages.SUCCESSFULLY_DATA_DELETED,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        messages.RESULT: messages.FAIL,
                        messages.MESSAGE: messages.DATA_NOT_EXISTS,
                    }, status=status.HTTP_200_OK)
        except Exception as ex:
            print('Exception',traceback.print_exc(ex))
            return Response({
                messages.RESULT: messages.FAIL,
                messages.MESSAGE: messages.SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)