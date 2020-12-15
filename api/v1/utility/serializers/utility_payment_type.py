from rest_framework import serializers, status
from django.db import transaction
from datetime import datetime
from v1.utility.models.utility_payment_type import UtilityPaymentType as UtilityPaymentTypeTbl


class UtilityPaymentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityPaymentTypeTbl
        fields = ('__all__')
