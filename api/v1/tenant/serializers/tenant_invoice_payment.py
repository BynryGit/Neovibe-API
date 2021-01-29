__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from api.messages import INVOICE_ALREADY_EXIST
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_invoice_payment import TenantInvoicePayment as TenantInvoicePaymentTbl
from v1.tenant.serializers.tenant_invoice import TenantInvoiceShortViewSerializer
from v1.tenant.views.common_functions import set_tenant_invoice_payment_validated_data


class TenantInvoicePaymentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    invoice_id = TenantInvoiceShortViewSerializer(many=False, required=False, source='get_invoice_id')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = TenantInvoicePaymentTbl
        fields = ('id_string', 'payment_method', 'payment_channel', 'transaction_no', 'transaction_date', 'amount',
                  'tax_amount', 'currency', 'created_date', 'updated_date', 'invoice_id', 'tenant')


class TenantInvoicePaymentSerializer(serializers.ModelSerializer):
    invoice_id = serializers.UUIDField(required=True)
    transaction_no = serializers.CharField(required=True, max_length=200)
    amount = serializers.FloatField(required=True)
    tax_amount = serializers.FloatField(required=True)

    class Meta:
        model = TenantInvoicePaymentTbl
        fields = ('__all__')

    def create(self, validated_data, tenant_obj, user):
        validated_data = set_tenant_invoice_payment_validated_data(validated_data)
        if TenantInvoicePaymentTbl.objects.filter(tenant=tenant_obj, invoice_id=validated_data["invoice_id"]).exists():
            raise CustomAPIException(INVOICE_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_invoice_obj = super(TenantInvoicePaymentSerializer, self).create(validated_data)
            tenant_invoice_obj.tenant = tenant_obj
            tenant_invoice_obj.created_by = user.id
            tenant_invoice_obj.save()
            return tenant_invoice_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tenant_invoice_payment_validated_data(validated_data)
        with transaction.atomic():
            tenant_invoice_obj = super(TenantInvoicePaymentSerializer, self).update(instance, validated_data)
            tenant_invoice_obj.updated_date = timezone.now()
            tenant_invoice_obj.save()
            return tenant_invoice_obj
