from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.utility.models.utility_service import get_utility_service_by_id_string
from v1.consumer.models.offer_type import get_offer_type_by_id_string


class CustomFilter:

    @staticmethod
    def get_filtered_queryset(queryset, request):
        if 'service_id' in request.query_params:
            service = get_utility_service_by_id_string(request.query_params['service_id'])
            queryset = queryset.filter(service_id=service.id)

        if 'utility_product_id' in request.query_params:
            utility_service_type_obj = get_utility_product_by_id_string(request.query_params['utility_product_id'])
            queryset = queryset.filter(utility_product_id=utility_service_type_obj.id)

        return queryset

    @staticmethod
    def get_offer_filtered_queryset(queryset, request):
        if 'offer_type_id' in request.query_params:
            offer_type = get_offer_type_by_id_string(request.query_params['offer_type_id'])
            queryset = queryset.filter(offer_type_id=offer_type.id)
        return queryset
