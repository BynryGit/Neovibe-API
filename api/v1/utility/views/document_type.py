__author__ = "aki"

from rest_framework import generics, status
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.document_type import DocumentType
from v1.commonapp.serializers.document_type import DocumentTypeListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_master import get_utility_by_id_string
from rest_framework.exceptions import APIException


class UtilityDocumentTypeList(generics.ListAPIView):
    try:
        serializer_class = DocumentTypeListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = DocumentType.objects.filter(utility=utility, is_active=True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Document types not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='UTILITY/DOCUMENT-TYPE')
        raise APIException
