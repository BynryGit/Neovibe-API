from rest_framework import serializers, status
from v1.consumer.serializers.service_sub_type import ServiceSubTypeListSerializer
from v1.service.models.consumer_service_master import ConsumerServiceMaster as ConsumerServiceMasterTbl
from api.messages import SERVICE_ALREADY_EXIST
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.service.views.common_functions import set_consumer_service_master_validated_data


class ConsumerServiceMasterShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerServiceMasterTbl
        fields = ('id_string', 'name')


class ConsumerServiceMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerServiceMasterTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class ConsumerServiceMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    service_type_id = serializers.CharField(required=False, max_length=200)
    service_sub_type_id = serializers.CharField(required=False, max_length=200)
    # utility_service_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerServiceMasterTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_service_master_validated_data(validated_data)
            if ConsumerServiceMasterTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SERVICE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_service_master_obj = super(ConsumerServiceMasterSerializer, self).create(validated_data)
                consumer_service_master_obj.created_by = user.id
                consumer_service_master_obj.updated_by = user.id
                consumer_service_master_obj.save()
                return consumer_service_master_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_service_master_validated_data(validated_data)
        with transaction.atomic():
            consumer_service_master_obj = super(ConsumerServiceMasterSerializer, self).update(instance, validated_data)
            consumer_service_master_obj.updated_by = user.id
            consumer_service_master_obj.updated_date = datetime.utcnow()
            consumer_service_master_obj.save()
            return consumer_service_master_obj


class ConsumerServiceMasterListSerializer(serializers.ModelSerializer):
    service_sub_type = ServiceSubTypeListSerializer(source='get_service_sub_type')

    class Meta:
        model = ConsumerServiceMasterTbl
        fields = ('id_string', 'name', 'service_sub_type', 'created_by', 'created_date')
