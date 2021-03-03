from rest_framework import serializers
from v1.utility.models.utility_work_order_type import UtilityWorkOrderType as UtilityWorkOrderTypeTbl


class UtilityWorkOrderTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityWorkOrderTypeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date')