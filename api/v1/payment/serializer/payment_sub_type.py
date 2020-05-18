from rest_framework import serializers
from v1.payment.models.payment_sub_type import PaymentSubType


class PaymentSubTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentSubType
        fields = ('name', 'id_string')


class PaymentSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = PaymentSubType
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')