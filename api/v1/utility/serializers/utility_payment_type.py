from rest_framework import serializers, status
from v1.payment.serializer.payment_type import PaymentTypeListSerializer
from v1.utility.models.utility_payment_type import UtilityPaymentType as UtilityPaymentTypeTbl


class UtilityPaymentTypeListSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeListSerializer(source='get_payment_type')

    class Meta:
        model = UtilityPaymentTypeTbl
        fields = ('id_string', 'name', 'payment_type')
