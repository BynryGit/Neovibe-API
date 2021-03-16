from datetime import datetime
from django.db import transaction
from rest_framework import serializers, status
from api.messages import CONTRACT_ALREADY_EXISTS
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail
from v1.consumer.views.common_functions import set_consumer_service_contract_detail_validated_data
from v1.utility.serializers.utility_service_contract_master import UtilityServiceContractMasterListSerializer
from v1.meter_data_management.serializers.meter import MeterViewSerializer
from v1.consumer.serializers.consumer_master import ConsumerViewSerializer
from v1.registration.serializers.registration import ChoiceField


class ConsumerServiceContractDetailViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    contract = UtilityServiceContractMasterListSerializer(source='get_contract')
    consumer_id = ConsumerViewSerializer(source='get_consumer_number')
    state = ChoiceField(choices=ConsumerServiceContractDetail.STATUS)
    meter_id = MeterViewSerializer(required=False, source='get_meter_number')

    class Meta:
        model = ConsumerServiceContractDetail
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'state', 'consumer_id', 'consumer_no', 'contract', 'meter_id','created_date')
        
# class ConsumerServiceContractDetailViewSerializer(serializers.ModelSerializer):
#     tenant = serializers.ReadOnlyField(source='tenant.name')
#     tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
#     utility = serializers.ReadOnlyField(source='utility.name')
#     utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
#     contract = UtilityServiceContractMasterListSerializer(source='get_contract')
#     consumer_id = ConsumerViewSerializer(many=False, source='get_consumer_number')
#     meter_id = MeterViewSerializer(many=False, source='get_meter_number')
#     status = ChoiceField(choices=ConsumerServiceContractDetail.STATUS)

#     class Meta:
#         model = ConsumerServiceContractDetail
#         fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_no', 'contract'
#                   'consumer_id', 'meter_id', 'status')


class ConsumerServiceContractDetailSerializer(serializers.ModelSerializer):
    service_contract_id = serializers.CharField(required=False, max_length=200)
    premise_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerServiceContractDetail
        fields = '__all__'

    def create(self, validated_data, consumer, user):
        validated_data = set_consumer_service_contract_detail_validated_data(validated_data)
        if ConsumerServiceContractDetail.objects.filter(consumer_id=consumer.id,
                                                        service_contract_id=validated_data['service_contract_id'],
                                                        premise_id=validated_data['premise_id']).exists():
            raise CustomAPIException(CONTRACT_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                consumer_service_contract_detail_obj = super(ConsumerServiceContractDetailSerializer, self).create(
                    validated_data)
                consumer_service_contract_detail_obj.tenant = consumer.tenant
                consumer_service_contract_detail_obj.utility = consumer.utility
                consumer_service_contract_detail_obj.consumer_no = consumer.consumer_no
                consumer_service_contract_detail_obj.consumer_id = consumer.id
                consumer_service_contract_detail_obj.is_active = True
                consumer_service_contract_detail_obj.created_by = user.id
                consumer_service_contract_detail_obj.created_date = datetime.now()
                consumer_service_contract_detail_obj.save()
                return consumer_service_contract_detail_obj
