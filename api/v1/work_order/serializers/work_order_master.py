from rest_framework import serializers

from v1.commonapp.serializers.service_request_type import ServiceTypeListSerializer
from v1.work_order.models.work_order_master import WorkOrderMaster as WorkOrderMasterTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import WORK_ORDER_ALREADY_EXIST
from v1.work_order.views.common_functions import set_work_order_validated_data
from v1.commonapp.serializers.service_request_sub_type import ServiceSubTypeListSerializer,ServiceSubTypeShortListSerializer
from rest_framework import status
from v1.service.serializers.consumer_service_master import ConsumerServiceMasterListSerializer
import json


class WorkOrderMasterShortListSerializer(serializers.ModelSerializer):
    # service_type_id = ServiceTypeListSerializer(source='get_service_type')
    # service_subtype_id = ServiceSubTypeShortListSerializer(source='get_service_subtype')
    class Meta:
        model = WorkOrderMasterTbl
        fields = ('name', 'id_string','description','json_obj')


class WorkOrderMasterListSerializer(serializers.ModelSerializer):
    work_order_master = ConsumerServiceMasterListSerializer(source='get_consumer_service_master')

    class Meta:
        model = WorkOrderMasterTbl
        fields = (
            'name', 'json_obj', 'id_string', 'description', 'work_order_master', 'created_date', 'is_active',
            'created_by')


class WorkOrderMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')


    class Meta:
        model = WorkOrderMasterTbl
        fields = (
            'id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date',
            'json_obj')


class WorkOrderMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    json_obj = serializers.JSONField(required=False)
    consumer_service_master_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = WorkOrderMasterTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_work_order_validated_data(validated_data)
            if WorkOrderMasterTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                 utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(WORK_ORDER_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                work_order_obj = super(WorkOrderMasterSerializer, self).create(validated_data)
                work_order_obj.created_by = user.id
                work_order_obj.updated_by = user.id
                # work_order_obj.json_obj = json.dumps(json_obj)
                work_order_obj.save()
                return work_order_obj

    def update(self, instance, validated_data, user):
        validated_data = set_work_order_validated_data(validated_data)
        with transaction.atomic():
            work_order_obj = super(WorkOrderMasterSerializer, self).update(instance, validated_data)
            work_order_obj.updated_by = user.id
            work_order_obj.updated_date = datetime.utcnow()
            work_order_obj.save()
            return work_order_obj
