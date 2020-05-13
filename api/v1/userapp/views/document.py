from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.userapp.models.user_master import get_documents_by_user_id_string
from v1.userapp.serializers.document import DocumentListSerializer

# API Header
# API end Point: api/v1/user/documents
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View, Add, Edit documents details of users
# Usage: This will display all documents of user.
# Tables used: 2.12.13. Lookup - Document
# Author: Arpita
# Created on: 13/05/2020


class Document(generics.ListAPIView):
    serializer_class = DocumentListSerializer

    def get_queryset(self):

        queryset = get_documents_by_user_id_string(1)
        return queryset
