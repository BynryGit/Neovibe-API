from django.db import transaction
from django.dispatch import receiver
from rest_framework import status
from django.dispatch import receiver, Signal
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.serializers.meter import MeterSerializer
from v1.work_order.views.common_functions import set_installation_service_contract_data, set_disconnection_service_contract_data
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailSerializer
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id
from v1.meter_data_management.models.meter import get_meter_by_number

installation_complete_service_appointment = Signal()
disconnection_complete_service_appointment = Signal()

# Signal receiver for consumer
@receiver([installation_complete_service_appointment, ])
def complete_installation_service_appointment(sender,key, **kwargs):
    try:
        if key == 'NEW_METER':
            meter_obj = super(MeterSerializer, MeterSerializer()).create(kwargs['data'])
            if meter_obj:
                data = set_installation_service_contract_data(sender,meter_obj)
                service_contract_obj = get_consumer_service_contract_detail_by_id(sender.consumer_service_contract_detail_id)
                contract_obj = super(ConsumerServiceContractDetailSerializer, ConsumerServiceContractDetailSerializer()).update(service_contract_obj,data)
        elif key == 'EXISTING_METER':
            meter_obj = get_meter_by_number(sender.completed_task_details['meter_no'])
            if meter_obj: 
                data = set_installation_service_contract_data(sender,meter_obj)
                service_contract_obj = get_consumer_service_contract_detail_by_id(sender.consumer_service_contract_detail_id)
                contract_obj = super(ConsumerServiceContractDetailSerializer, ConsumerServiceContractDetailSerializer()).update(service_contract_obj,data)
            else:
                raise CustomAPIException("Error in creating meter",
                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print('===',e)
        raise CustomAPIException("Error in creating meter installation signal",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@receiver([disconnection_complete_service_appointment, ])
def complete_disconnection_service_appointment(sender, **kwargs):
    try:
        if kwargs['key'] == 'PERMANENT':
            data = set_disconnection_service_contract_data(sender,'PERMANENT')
        elif kwargs['key'] == 'TEMPORARY':
            data = set_disconnection_service_contract_data(sender,'TEMPORARY')
        service_contract_obj = get_consumer_service_contract_detail_by_id(sender.consumer_service_contract_detail_id)
        contract_obj = super(ConsumerServiceContractDetailSerializer, ConsumerServiceContractDetailSerializer()).update(service_contract_obj,data)
        
    except Exception as e:
        print('===',e)
        raise CustomAPIException("Error in creating meter disconnection signal ",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
