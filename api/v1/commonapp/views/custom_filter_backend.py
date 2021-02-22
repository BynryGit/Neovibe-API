from v1.meter_data_management.models.schedule import get_schedule_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.consumer.models.consumer_master import ConsumerMaster, get_consumer_by_id_string
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail

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

        if 'consumer_processing' in request.query_params:
            consumer_master_list = []
            consumer_master_objs = ConsumerMaster.objects.filter(is_active=True, state=0)
            if consumer_master_objs:
                for consumer_master_obj in consumer_master_objs:
                    consumer_master_list.append(consumer_master_obj)
                    # consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerServiceContractDetail.objects.filter(consumer_id__in=[consumer.id for consumer in consumer_master_list], is_active=False, state=0)
                    # queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
        
        if 'consumer_id' in request.query_params:
            consumer = get_consumer_by_id_string(request.query_params['consumer_id'])
            queryset = queryset.filter(consumer_id=consumer.id, is_active=True)
        return queryset

        return queryset
