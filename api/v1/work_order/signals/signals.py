from django.db import transaction
from django.dispatch import receiver
from rest_framework import status
from django.dispatch import receiver, Signal
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.serializers.meter import MeterSerializer
from v1.work_order.views.common_functions import set_consumer_service_contract_data
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailSerializer
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id

complete_service_appointment = Signal()

# Signal receiver for consumer
@receiver([complete_service_appointment, ])
def after_complete_service_appointment(sender, **kwargs):
    try:
        meter_obj = super(MeterSerializer, MeterSerializer()).create(kwargs['data'])
        service_contract_obj = get_consumer_service_contract_detail_by_id(sender.consumer_service_contract_detail_id)
        data = set_consumer_service_contract_data(sender,meter_obj)
        contract_obj = super(ConsumerServiceContractDetailSerializer, ConsumerServiceContractDetailSerializer()).update(service_contract_obj,data)
    except Exception as e:
        print('===',e)
        raise CustomAPIException("Error in creating meter",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
