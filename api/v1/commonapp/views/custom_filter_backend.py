from v1.meter_data_management.models.schedule import get_schedule_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.commonapp.models.module import get_module_by_id_string


class CustomFilter:

    @staticmethod
    def get_filtered_queryset(queryset, request):
        if 'product_id' in request.query_params:
            product = get_utility_product_by_id_string(request.query_params['product_id'])
            queryset = queryset.filter(service_id=product.id)

        if 'utility_product_id' in request.query_params:
            utility_service_type_obj = get_utility_product_by_id_string(request.query_params['utility_product_id'])
            queryset = queryset.filter(utility_product_id=utility_service_type_obj.id)

        if 'schedule_id' in request.query_params:
            schedule_obj = get_schedule_by_id_string(request.query_params['schedule_id'])
            queryset = queryset.filter(schedule_id=schedule_obj.id)

        if 'module_id' in request.query_params:
            module_obj = get_module_by_id_string(request.query_params['module_id'])
            queryset = queryset.filter(module_id=module_obj.id)

        return queryset
