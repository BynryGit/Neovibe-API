from rest_framework import serializers
from v1.utility.models.utility_work_order_sub_type import UtilityWorkOrderSubType as UtilityWorkOrderSubTypeTbl
from v1.commonapp.serializers.work_order_sub_type import WorkOrderSubTypeListSerializer
from v1.utility.serializers.utility_work_order_type import UtilityWorkOrderTypeListSerializer


class UtilityWorkOrderSubTypeListSerializer(serializers.ModelSerializer):
    work_order_sub_type = WorkOrderSubTypeListSerializer(source='get_work_order_sub_type')
    utility_work_order_type = UtilityWorkOrderTypeListSerializer(source='get_utility_work_order_type')

    class Meta:
        model = UtilityWorkOrderSubTypeTbl
        fields = ('name', 'id_string', 'work_order_sub_type', 'utility_work_order_type', 'is_active', 'created_by', 'created_date')
