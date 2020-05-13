from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.userapp.models.user_master import get_notes_by_user_id_string
from v1.userapp.serializers.notes import NoteListSerializer

# API Header
# API end Point: api/v1/user/notes
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View notes of users
# Usage: This will display all notes of user.
# Tables used: 2.5.12. Lookup - Notes
# Author: Arpita
# Created on: 13/05/2020


class Note(generics.ListAPIView):
    serializer_class = NoteListSerializer

    def get_queryset(self):

        queryset = get_notes_by_user_id_string(1)
        return queryset
