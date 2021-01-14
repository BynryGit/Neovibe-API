__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from api.messages import INVOICE_ALREADY_EXIST
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_invoice import TenantInvoice as TenantInvoiceTbl
from v1.tenant.serializers.tenant_bank_detail import TenantBankDetailShortViewSerializer
from v1.tenant.serializers.tenant_subscription import TenantSubscriptionShortViewSerializer
from v1.tenant.views.common_functions import set_tenant_invoice_validated_data


class TenantInvoiceShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantInvoiceTbl
        fields = ('id_string', 'invoice_number', 'invoice_date', 'invoice_amt', 'invoice_tax')


class TenantInvoiceViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    tenant_subscription_id = TenantSubscriptionShortViewSerializer(many=False, required=False, source='get_tenant_subscription_id')
    tenant_bank_detail_id = TenantBankDetailShortViewSerializer(many=False, required=False, source='get_tenant_bank_detail_id')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantInvoiceTbl
        fields = ('id_string', 'invoice_number', 'invoice_date', 'invoice_amt', 'invoice_tax', 'invoice_url',
                  'due_date', 'contact_name', 'contact_no', 'email_id', 'month', 'billing_address', 'address',
                  'created_date', 'updated_date', 'tenant_subscription_id', 'tenant_bank_detail_id', 'tenant')


class TenantInvoiceSerializer(serializers.ModelSerializer):
    tenant_subscription_id = serializers.UUIDField(required=True)
    tenant_bank_detail_id  = serializers.UUIDField(required=True)
    invoice_number = serializers.CharField(required=True, max_length=200)
    invoice_amt  = serializers.FloatField(required=True)
    email_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = TenantInvoiceTbl
        fields = ('__all__')

    def create(self, validated_data, tenant_obj, user):
        validated_data = set_tenant_invoice_validated_data(validated_data)
        if TenantInvoiceTbl.objects.filter(tenant=tenant_obj,
                                           tenant_subscription_id=validated_data["tenant_subscription_id"],
                                           invoice_number=validated_data["invoice_number"]).exists():
            raise CustomAPIException(INVOICE_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_invoice_obj = super(TenantInvoiceSerializer, self).create(validated_data)
            tenant_invoice_obj.tenant = tenant_obj
            tenant_invoice_obj.created_by = user.id
            tenant_invoice_obj.save()
            return tenant_invoice_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tenant_invoice_validated_data(validated_data)
        with transaction.atomic():
            tenant_invoice_obj = super(TenantInvoiceSerializer, self).update(instance, validated_data)
            tenant_invoice_obj.updated_date = timezone.now()
            tenant_invoice_obj.save()
            return tenant_invoice_obj
