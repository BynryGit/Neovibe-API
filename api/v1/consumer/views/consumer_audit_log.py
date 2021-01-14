from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter

from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.audit_log import AuditLog
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.serializers.audit_log import AuditLogViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.consumer.models.consumer_master import get_consumer_by_id_string


class ConsumerAuditLogList(generics.ListAPIView):
    try:
        serializer_class = AuditLogViewSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('tenant__id_string',)
        ordering_fields = ('tenant',)
        search_fields = ('tenant__name',)

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1, 1, 1, user_obj):
                    consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    queryset = AuditLog.objects.filter(utility=consumer.utility, is_active=True, object_id=consumer.id,
                                                       module_id=get_module_by_key("CONSUMEROPS"),
                                                       sub_module_id=get_sub_module_by_key("CONSUMER"))
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Consumer Audit logs not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module='Consumer ops', sub_module='Consumer')