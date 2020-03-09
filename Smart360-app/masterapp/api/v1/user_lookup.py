__author__ = "Arpita"

from rest_framework.views import APIView
from masterapp.models.user_lookup import Privilege


class PrivilegeApiView(APIView):
    """Privilege Api View"""
    def get(self, request, format=None):
        print(request.data)

        serializer = UserProfileSerializer(data=request.data)

    def post(self, request, format=None):
        print(request.data)

    def put(self, request, format=None):
        print(request.data)

    def delete(self, request, format=None):
        print(request.data)