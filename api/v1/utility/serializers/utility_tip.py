from rest_framework import serializers
from v1.utility.models.utility_tip import UtilityTip


class UtilityTipListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityTip
        fields = ('tenant', 'tenant_id_string', 'utility', 'utility_id_string', "tip", "description")
