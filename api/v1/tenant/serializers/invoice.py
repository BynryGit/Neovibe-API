import uuid
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.tenant.models.tenant_invoices import TenantInvoices
from v1.tenant.views.common_functions import set_validated_data

class TenantInvoiceListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantInvoices
        fields = ('id_string', 'tenant', 'subscription_id', 'tenantbankdetails_id', 'invoice_number',
                  'invoice_date', 'invoice_amt', 'invoice_tax', 'invoice_url', 'due_date',
                  'contact_name', 'contact_no', 'email_id', 'month', 'billing_address', 'address', 'is_active')

class TenantInvoiceViewSerializer(serializers.ModelSerializer):
    #status = TenantStatusViewSerializer(many=False, source='get_status')
    # area = AreaListSerializer(many=False, source='get_area')
    # tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantInvoices
        fields = ('id_string',  'tenant','subscription_id','tenantbankdetails_id','invoice_number',
                    'invoice_date','invoice_amt','invoice_tax','invoice_url','due_date',
                  'contact_name','contact_no','email_id','month','billing_address','address', 'is_active')


class TenantInvoiceSerializer(serializers.ModelSerializer):
    id_string = serializers.CharField(required=False, max_length=200)
    tenant = serializers.CharField(required=False, max_length=200)
    subscription_id = serializers.CharField(required=False, max_length=200)
    tenantbankdetails_id  = serializers.CharField(required=False, max_length=200)
    invoice_number = serializers.CharField(required=False, max_length=200)
    invoice_date  = serializers.CharField(required=False, max_length=200)
    invoice_amt  = serializers.CharField(required=False, max_length=200)
    invoice_tax  = serializers.CharField(required=False, max_length=200)
    invoice_url  = serializers.CharField(required=False, max_length=200)
    due_date  = serializers.CharField(required=False, max_length=200)
    contact_name = serializers.CharField(required=False, max_length=200)
    contact_no  = serializers.CharField(required=False, max_length=200)
    email_id = serializers.CharField(required=False, max_length=200)
    month  = serializers.CharField(required=False, max_length=200)
    billing_address  = serializers.CharField(required=False, max_length=200)
    address = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantInvoices
        fields = ('__all__')

    def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_invoicce_obj = super(TenantInvoiceSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            tenant_invoicce_obj.save()
            return tenant_invoicce_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_invoice_obj = super(TenantInvoiceSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            tenant_invoice_obj.save()
            return tenant_invoice_obj