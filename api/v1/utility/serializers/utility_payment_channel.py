from rest_framework import serializers
from v1.utility.models.utility_payment_channel import UtilityPaymentChannel as UtilityPaymentChannelTbl


class UtilityPaymentChannelListSerializer(serializers.ModelSerializer):
    utility = serializers.ReadOnlyField(source='utility.name')

    class Meta:
        model = UtilityPaymentChannelTbl
        fields = ('utility', 'name', 'id_string', 'is_active', 'created_by', 'created_date')
