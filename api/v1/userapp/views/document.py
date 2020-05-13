from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

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


class Document(GenericAPIView):

    def get(self, request, id_string):
        try:
            bank = get_bank_by_user_id_string(id_string)
            if bank:
                serializer = BankViewSerializer(instance=bank, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)