from v1.utility.models.utility_service import get_utility_service_by_id_string


class CustomFilter:

    @staticmethod
    def get_filtered_queryset(queryset, request):
        if 'service_id' in request.query_params:
            service = get_utility_service_by_id_string(request.query_params['service_id'])
            queryset = queryset.filter(service_id=service.id)

        return queryset
