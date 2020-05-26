__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_invoice import SupplierInvoice as SupplierInvoiceTbl
from v1.supplier.views.common_functions import set_supplier_invoice_validated_data


class SupplierInvoiceViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    due_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    invoice_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = SupplierInvoiceTbl
        fields = ('id_string', 'invoice_no', 'invoice_amount', 'invoice_date', 'due_date', 'created_date', 'updated_date',
                  'tenant', 'utility', 'contract', 'supplier', 'supplier_financial', 'demand', 'status_id')


class SupplierInvoiceSerializer(serializers.ModelSerializer):
    contract = serializers.UUIDField(required=False)
    supplier_financial = serializers.UUIDField(required=False)
    demand = serializers.UUIDField(required=False)
    invoice_no = serializers.CharField(required=True, max_length=500)
    invoice_amount = serializers.FloatField(required=True)

    class Meta:
        model = SupplierInvoiceTbl
        fields = ('__all__')

    def create(self, validated_data, supplier_obj, user):
        validated_data = set_supplier_invoice_validated_data(validated_data)
        if SupplierInvoiceTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             supplier=supplier_obj.id, invoice_no=validated_data["invoice_no"]).exists():
            return False
        with transaction.atomic():
            utility_obj = super(SupplierInvoiceSerializer, self).create(validated_data)
            utility_obj.tenant = user.tenant
            utility_obj.utility = user.utility
            utility_obj.supplier = supplier_obj.id
            utility_obj.created_by = user.id
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_invoice_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierInvoiceSerializer, self).update(instance, validated_data)
            utility_obj.tenant = user.tenant
            utility_obj.utility = user.utility
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.save()
            return utility_obj