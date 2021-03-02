__author__ = "chinmay"

from rest_framework import serializers, status
from v1.commonapp.models.work_order_sub_type import WorkOrderSubType as WorkOrderSubTypeTbl
from django.db import transaction
from v1.commonapp.common_functions import set_work_order_sub_type_validated_data
from datetime import datetime
from api.messages import WORK_ORDER_SUB_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.serializers.work_order_type import WorkOrderTypeListSerializer
from v1.utility.models.utility_work_order_sub_type import UtilityWorkOrderSubType as UtilityWorkOrderSubTypeTbl


class WorkOrderSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityWorkOrderSubTypeTbl
        fields = '__all__'


class WorkOrderSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    work_order_sub_type_id = serializers.CharField(required=False, max_length=200)
    utility_work_order_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityWorkOrderSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_work_order_sub_type_validated_data(validated_data)
            if UtilityWorkOrderSubTypeTbl.objects.filter(name=validated_data['name'],
                                                         tenant_id=validated_data['tenant_id'],
                                                         utility_id=validated_data['utility_id'],
                                                         utility_work_order_type_id=validated_data['utility_work_order_type_id']).exists():
                raise CustomAPIException(WORK_ORDER_SUB_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                work_order_sub_type_obj = super(WorkOrderSubTypeSerializer, self).create(validated_data)
                work_order_sub_type_obj.created_by = user.id
                work_order_sub_type_obj.save()
                return work_order_sub_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_work_order_sub_type_validated_data(validated_data)
        with transaction.atomic():
            work_order_sub_type_obj = super(WorkOrderSubTypeSerializer, self).update(instance, validated_data)
            work_order_sub_type_obj.tenant = user.tenant
            work_order_sub_type_obj.updated_by = user.id
            work_order_sub_type_obj.updated_date = datetime.utcnow()
            work_order_sub_type_obj.save()
            return work_order_sub_type_obj


class WorkOrderSubTypeListSerializer(serializers.ModelSerializer):
    work_order_type = WorkOrderTypeListSerializer(source='get_work_order_type')

    class Meta:
        model = WorkOrderSubTypeTbl
        fields = ('name', 'id_string', 'work_order_type', 'is_active', 'created_by', 'created_date')
