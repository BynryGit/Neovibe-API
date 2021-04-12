from rest_framework import generics, status
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.currency import Currency
from v1.commonapp.serializers.currency import CurrencyListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination


class CurrencyList(generics.ListAPIView):
    try:
        serializer_class = CurrencyListSerializer
        pagination_class = StandardResultsSetPagination

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    queryset = Currency.objects.all()
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Currencies not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Commonapp', sub_module='Commonapp')
