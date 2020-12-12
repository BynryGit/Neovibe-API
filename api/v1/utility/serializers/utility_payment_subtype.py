from rest_framework import serializers, status
from django.db import transaction
from datetime import datetime
from v1.utility.models.utility_payment_subtype import UtilityPaymentSubtype as UtilityPaymentSubtypeTbl
from v1.payment.serializer.payment_type import PaymentTypeListSerializer
from v1.utility.serializers.utility_payment_type import UtilityPaymentTypeListSerializer



class UtilityPaymentSubtypeListSerializer(serializers.ModelSerializer):
    payment_type = UtilityPaymentTypeListSerializer(many=True,source="get_payment_type")


    
    class Meta:
        model = UtilityPaymentSubtypeTbl
        fields = ('name', 'id_string','is_active','created_by','created_date','payment_type','gl_code','tax')
