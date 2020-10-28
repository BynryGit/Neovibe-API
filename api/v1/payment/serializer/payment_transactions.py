from django.db import transaction
from rest_framework import serializers
from v1.payment.models.payment_transactions import PaymentTransaction
from v1.payment.views.common_functions import set_payment_transaction_validated_data


class PaymentTransactionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTransaction
        fields = ('__all__')


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
