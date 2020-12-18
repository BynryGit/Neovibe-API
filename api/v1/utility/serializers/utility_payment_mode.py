from rest_framework import serializers, status
from django.db import transaction
from datetime import datetime
from v1.utility.models.utility_payment_mode import UtilityPaymentMode as UtilityPaymentModeTbl
from v1.payment.serializer.payment_type import PaymentTypeListSerializer


class UtilityPaymentModeListSerializer(serializers.ModelSerializer):
    key = serializers.ReadOnlyField(source='get_payment_mode_key')

    class Meta:
        model = UtilityPaymentModeTbl
        fields = ('name', 'id_string', 'key', 'is_active', 'created_by', 'created_date')
