__author__ = "chinmay"

from rest_framework import serializers, status
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from v1.commonapp.models.work_order_type import WorkOrderType as WorkOrderTypeTbl
from django.db import transaction
from v1.commonapp.common_functions import set_work_order_type_validated_data
from datetime import datetime
from api.messages import WORK_ORDER_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_work_order_type import UtilityWorkOrderType as UtilityWorkOrderTypeTbl


class WorkOrderTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityWorkOrderTypeTbl
        fields = '__all__'


class WorkOrderTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    work_order_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityWorkOrderTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_work_order_type_validated_data(validated_data)
            if UtilityWorkOrderTypeTbl.objects.filter(name=validated_data['name'],
                                                      tenant_id=validated_data['tenant_id'],
                                                      utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(WORK_ORDER_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                work_order_type_obj = super(WorkOrderTypeSerializer, self).create(validated_data)
                work_order_type_obj.created_by = user.id
                work_order_type_obj.save()
                return work_order_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_work_order_type_validated_data(validated_data)
        with transaction.atomic():
            work_order_type_obj = super(WorkOrderTypeSerializer, self).update(instance, validated_data)
            work_order_type_obj.tenant = user.tenant
            work_order_type_obj.updated_by = user.id
            work_order_type_obj.updated_date = datetime.utcnow()
            work_order_type_obj.save()
            return work_order_type_obj


class WorkOrderTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderTypeTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')
