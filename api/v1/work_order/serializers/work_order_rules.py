from rest_framework import serializers
from v1.work_order.models.work_order_rules import WorkOrderRule as WorkOrderRuleTbl


class WorkOrderListSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = WorkOrderRuleTbl
        fields = ('utility','rule', 'id_string', 'is_active', 'created_by', 'created_date')