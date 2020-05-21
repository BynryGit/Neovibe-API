import uuid
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.tenant.models.tenant_invoice_payment import TenantInvoicePayment
from v1.tenant.views.common_functions import set_validated_data

class TenantInvoicePaymentListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantInvoicePayment
        fields = ('id_string', 'tenant', 'invoice_number', 'payment_method', 'payment_channel',
                  'transaction_no', 'transaction_date', 'amount', 'tax_amount', 'currency', 'is_active')

class TenantInvoicePaymentViewSerializer(serializers.ModelSerializer):
    #status = TenantStatusViewSerializer(many=False, source='get_status')
    # area = AreaListSerializer(many=False, source='get_area')
    # tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantInvoicePayment
        fields = ('id_string',  'tenant','invoice_number','payment_method','payment_channel',
                    'transaction_no', 'transaction_date','amount','tax_amount','currency', 'is_active')


class TenantInvoicePaymentSerializer(serializers.ModelSerializer):
    id_string = serializers.CharField(required=False, max_length=200)
    tenant  = serializers.CharField(required=False, max_length=200)
    invoice_number  = serializers.CharField(required=False, max_length=200)
    payment_method  = serializers.CharField(required=False, max_length=200)
    payment_channel  = serializers.CharField(required=False, max_length=200)
    transaction_no = serializers.CharField(required=False, max_length=200)
    transaction_date  = serializers.CharField(required=False, max_length=200)
    amount = serializers.CharField(required=False, max_length=200)
    tax_amount  = serializers.CharField(required=False, max_length=200)
    currency  = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantInvoicePayment
        fields = ('__all__')

    def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_invoice_payment_obj = super(TenantInvoicePaymentSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            tenant_invoice_payment_obj.save()
            return tenant_invoice_payment_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_invoice_payment_obj = super(TenantInvoicePaymentSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            tenant_invoice_payment_obj.save()
            return tenant_invoice_payment_obj