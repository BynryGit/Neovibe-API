import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.userapp.models.user_master import get_notes_by_user_id_string, get_user_by_id_string
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
from v1.userapp.views.common_functions import is_note_data_verified, add_note_document, save_edited_note


class Note(generics.ListAPIView):
    serializer_class = NoteListSerializer

    def get_queryset(self):

        queryset = get_notes_by_user_id_string(1)
        return queryset


# API Header
# API end Point: api/v1/user/note
# API verb: POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Add user notes, Edit user notes
# Usage: Add, Edit User notes
# Tables used: 2.5.12. Lookup - Notes
# Author: Arpita
# Created on: 14/05/2020

class UserDocument(GenericAPIView):

    def post(self, request, format=None):
        try:

            # Request data verification start
            if is_note_data_verified(request):
                # Request data verification end

                # Save basic user details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = add_note_document(request, user)
                if result:
                    data = {
                        "user_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Save basic role details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:

            # Request data verification start
            if is_note_data_verified(request):
                # Request data verification end

                # Edit basic details start
                user = get_user_by_id_string(request.data['user'])
                user_detail, result, error = save_edited_note(request, user)
                if result:
                    data = {
                        "user_detail_id_string": user_detail.id_string
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        ERROR: error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Edit basic details start
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
