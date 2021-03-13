from v1.meter_data_management.models.schedule import get_schedule_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.consumer.models.consumer_master import ConsumerMaster, get_consumer_by_id_string
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail
from v1.commonapp.models.module import get_module_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string , ConsumerMaster
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail
from v1.utility.models.utility_work_order_type import get_utility_work_order_type_by_id_string
from v1.complaint.models.complaint_type import get_complaint_type_by_id_string
from v1.work_order.models.service_appointments import ServiceAppointment
from v1.commonapp.models.work_order_type import get_work_order_type_by_key
from v1.commonapp.models.work_order_sub_type import get_work_order_sub_type_by_key
from v1.utility.models.utility_work_order_type import get_utility_work_order_type_by_id
from v1.utility.models.utility_work_order_sub_type import get_utility_work_order_sub_type_by_id
from v1.work_order.models.work_order_master import get_work_order_master_by_id, WorkOrderMaster, get_work_order_master_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.utility.models.utility_module import get_utility_module_by_id_string


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

        if 'category_id' in request.query_params:
            consumer_category = get_consumer_category_by_id_string(request.query_params['category_id'])
            queryset = queryset.filter(category_id=consumer_category.id)

        if 'utility_work_order_type_id' in request.query_params:
            utility_work_order_type = get_utility_work_order_type_by_id_string(request.query_params['utility_work_order_type_id'])
            queryset = queryset.filter(utility_work_order_type_id=utility_work_order_type.id)

        if 'complaint_type_id' in request.query_params:
            complaint_type = get_complaint_type_by_id_string(request.query_params['complaint_type_id'])
            queryset = queryset.filter(complaint_type_id=complaint_type.id)

        # if 'module_id' in request.query_params:
        #     module = get_utility_module_by_id_string(request.query_params['module_id'])
        #     queryset = queryset.filter(module_id=module.id)


        if 'consumer_processing' in request.query_params:
            consumer_master_list = []
            consumer_master_objs = ConsumerMaster.objects.filter(is_active=True, state=0)
            if consumer_master_objs:
                for consumer_master_obj in consumer_master_objs:
                    consumer_master_list.append(consumer_master_obj)
                    # consumer = get_consumer_by_id_string(self.kwargs['id_string'])
                    queryset = ConsumerServiceContractDetail.objects.filter(consumer_id__in=[consumer.id for consumer in consumer_master_list], is_active=False, state=2)
                    # queryset = CustomFilter.get_filtered_queryset(queryset, self.request)
        
        if 'consumer_id' in request.query_params:
            consumer = get_consumer_by_id_string(request.query_params['consumer_id'])
            queryset = ConsumerServiceContractDetail.objects.filter(consumer_id=consumer.id, is_active=True)
            if 'temporary_disconnected_meter' in request.query_params:
                queryset = queryset.filter(consumer_id=consumer.id, is_active=True, state=1)
            else:
                queryset = queryset.filter(consumer_id=consumer.id, is_active=True, state=0)

        if 'Disconnect_processing' in request.query_params:
            work_order_type_obj = get_work_order_type_by_key('DISCONNECTION')
            if work_order_type_obj:
                    utility_work_order_type_obj = get_utility_work_order_type_by_id(work_order_type_obj.id)
            if utility_work_order_type_obj:
                print("++++++++++++",utility_work_order_type_obj)
                work_order_master_obj = WorkOrderMaster.objects.filter(utility_work_order_type_id=utility_work_order_type_obj.id)
                if work_order_master_obj:
                    print("++++MASTER+++++++",work_order_master_obj)
                    queryset = ServiceAppointment.objects.filter(work_order_master_id__in = [ i.id for i in work_order_master_obj])
                    print("++++++++++",queryset)

        if 'Outage_processing' in request.query_params:
            work_order_type_obj = get_work_order_type_by_key('OUTAGE')
            if work_order_type_obj:
                    utility_work_order_type_obj = get_utility_work_order_type_by_id(work_order_type_obj.id)
            if utility_work_order_type_obj:
                print("++++++++++++",utility_work_order_type_obj)
                work_order_master_obj = WorkOrderMaster.objects.filter(utility_work_order_type_id=utility_work_order_type_obj.id)
                if work_order_master_obj:
                    print("++++MASTER+++++++",work_order_master_obj)
                    queryset = ServiceAppointment.objects.filter(work_order_master_id__in = [ i.id for i in work_order_master_obj])
                    print("++++++++++",queryset)
                    
        if 'Transfer_processing' in request.query_params:
            work_order_type_obj = get_work_order_type_by_key('TRANSFER')
            if work_order_type_obj:
                    utility_work_order_type_obj = get_utility_work_order_type_by_id(work_order_type_obj.id)
            if utility_work_order_type_obj:
                print("++++++++++++",utility_work_order_type_obj)
                work_order_master_obj = WorkOrderMaster.objects.filter(utility_work_order_type_id=utility_work_order_type_obj.id)
                if work_order_master_obj:
                    print("++++MASTER+++++++",work_order_master_obj)
                    queryset = ServiceAppointment.objects.filter(work_order_master_id__in = [ i.id for i in work_order_master_obj])
                    print("++++++++++",queryset)                     
        return queryset

