from rest_framework import serializers

# from v1.commonapp.serializers.service_request_type import ServiceTypeListSerializer
from v1.work_order.models.work_order_master import WorkOrderMaster as WorkOrderMasterTbl
from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import WORK_ORDER_ALREADY_EXIST
from v1.work_order.views.common_functions import set_work_order_validated_data
# from v1.commonapp.serializers.service_request_sub_type import ServiceSubTypeListSerializer,ServiceSubTypeShortListSerializer
from rest_framework import status
from v1.utility.serializers.utility_work_order_sub_type import UtilityWorkOrderSubTypeListSerializer
from v1.utility.serializers.utility_product import UtilityProductListSerializer
from v1.utility.models.utility_work_order_sub_type import get_utility_work_order_sub_type_by_id
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer


class WorkOrderMasterShortListSerializer(serializers.ModelSerializer):
    utility_product_id = UtilityProductShortViewSerializer(source='get_utility_product_by_id')
    utility_work_order_sub_type = UtilityWorkOrderSubTypeListSerializer(source='get_utility_work_order_sub_type')

    class Meta:
        model = WorkOrderMasterTbl
        fields = ('name', 'id_string', 'description', 'json_obj', 'utility_product_id', 'utility_work_order_sub_type', 'base_rate')


class WorkOrderMasterListSerializer(serializers.ModelSerializer):
    utility_work_order_sub_type = UtilityWorkOrderSubTypeListSerializer(source='get_utility_work_order_sub_type')
    utility_product = UtilityProductListSerializer(source='get_utility_product_by_id')

    class Meta:
        model = WorkOrderMasterTbl
        fields = (
            'name', 'json_obj', 'id_string', 'utility_work_order_sub_type', 'description', 'service_obj',
            'created_date', 'is_active',
            'created_by', 'utility_product', 'base_rate', 'tax_rate', 'is_taxable')


class WorkOrderMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    utility_work_order_sub_type = UtilityWorkOrderSubTypeListSerializer(source='get_utility_work_order_sub_type')

    class Meta:
        model = WorkOrderMasterTbl
        fields = (
            'id_string', 'name', 'tenant', 'utility_work_order_sub_type','description', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date',
            'json_obj','instructions')


class WorkOrderMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    json_obj = serializers.JSONField(required=False)
    utility_work_order_type_id = serializers.CharField(required=False, max_length=200)
    utility_work_order_sub_type_id = serializers.CharField(required=False, max_length=200)
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

                # work_order_obj.json_obj = json.dumps(json_obj)
                work_order_obj.save()
                return work_order_obj

    def update(self, instance, validated_data, user):
        validated_data = set_work_order_validated_data(validated_data)
        if WorkOrderMasterTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                             utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(WORK_ORDER_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                work_order_obj = super(WorkOrderMasterSerializer, self).update(instance, validated_data)
                work_order_obj.updated_by = user.id
                work_order_obj.updated_date = datetime.utcnow()
                work_order_obj.save()
                return work_order_obj
