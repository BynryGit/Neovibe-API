from rest_framework import serializers

from v1.meter_reading.models.bill_cycle import BillCycle


class BillCycleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillCycle
        fields = ('code', 'id_string')


class BillCycleViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = BillCycle
        fields = ('id_string', 'code', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')