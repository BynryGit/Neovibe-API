from rest_framework import serializers
from v1.utility.models.utility_payment_channel import UtilityPaymentChannel as UtilityPaymentChannelTbl
from v1.utility.serializers.utility_product import UtilityProductListSerializer


class UtilityPaymentChannelListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField(method_name='conversion_bool')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_product = UtilityProductListSerializer(source='get_utility_product')

    class Meta:
        model = UtilityPaymentChannelTbl
        fields = ('utility', 'name', 'id_string', 'utility_product', 'is_active', 'created_by', 'created_date')
