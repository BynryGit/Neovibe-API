from django.db import transaction
from rest_framework import serializers
from v1.payment.models.payment_transactions import PaymentTransaction
from v1.payment.serializer.payment_sub_type import PaymentSubTypeListSerializer
from v1.payment.serializer.payment_type import PaymentTypeListSerializer
from v1.payment.views.common_functions import set_payment_transaction_validated_data


class PaymentTransactionListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    transaction_type = PaymentTypeListSerializer(many=False, source='get_transaction_type')
    transaction_sub_type = PaymentSubTypeListSerializer(many=False, source='get_transaction_sub_type')

    class Meta:
        model = PaymentTransaction
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'transaction_type',
                  'transaction_sub_type', 'transaction_amount', 'tax_amount', 'transaction_date', 'created_date')


class PaymentTransactionSerializer(serializers.ModelSerializer):
    transaction_type_id = serializers.CharField(required=False, max_length=200)
    transaction_sub_type_id = serializers.CharField(required=False, max_length=200)
    transaction_amount = serializers.CharField(required=False, max_length=200)
    tax_amount = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = PaymentTransaction
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_payment_transaction_validated_data(validated_data)
        with transaction.atomic():
            payment_transaction = super(PaymentTransactionSerializer, self).create(validated_data)
            return payment_transaction
