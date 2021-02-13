from rest_framework import serializers, status
from v1.payment.serializer.payment_type import PaymentTypeListSerializer
from v1.utility.models.utility_payment_type import UtilityPaymentType as UtilityPaymentTypeTbl
from v1.utility.serializers.utility_product import UtilityProductListSerializer

class UtilityPaymentTypeListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField(method_name='conversion_bool')
    utility_product = UtilityProductListSerializer(source='get_utility_product')
    payment_type = PaymentTypeListSerializer(source='get_payment_type')

    class Meta:
        model = UtilityPaymentTypeTbl
        fields = ('id_string', 'name','utility_product', 'is_active', 'payment_type')

    def conversion_bool(self, instance):
        if instance.is_active:
            return "Yes"
        else:
            return "No"
