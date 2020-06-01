__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.contract.serializers.contract import ContractShortViewSerializer
from v1.contract.views.common_functions import set_contract_invoice_validated_data
from v1.supplier.models.supplier_invoice import SupplierInvoice as SupplierInvoiceTbl


class SupplierInvoiceViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    contract = ContractShortViewSerializer(many=False, required=False, source='get_contract')
    due_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    invoice_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = SupplierInvoiceTbl
        fields = ('id_string', 'invoice_no', 'invoice_amount', 'invoice_date', 'due_date', 'created_date', 'updated_date',
                  'tenant', 'utility', 'contract', 'demand', 'status_id')


class SupplierInvoiceSerializer(serializers.ModelSerializer):
    demand = serializers.UUIDField(required=False)
    invoice_no = serializers.CharField(required=True, max_length=500)
    invoice_amount = serializers.FloatField(required=True)

    class Meta:
        model = SupplierInvoiceTbl
        fields = ('__all__')

    def create(self, validated_data, contract_obj, user):
        validated_data = set_contract_invoice_validated_data(validated_data)
        if SupplierInvoiceTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             contract=contract_obj.id, invoice_no=validated_data["invoice_no"]).exists():
            return False
        with transaction.atomic():
            contract_invoice_obj = super(SupplierInvoiceSerializer, self).create(validated_data)
            contract_invoice_obj.tenant = user.tenant
            contract_invoice_obj.utility = user.utility
            contract_invoice_obj.contract = contract_obj.id
            contract_invoice_obj.created_by = user.id
            contract_invoice_obj.save()
            return contract_invoice_obj

    def update(self, instance, validated_data, user):
        validated_data = set_contract_invoice_validated_data(validated_data)
        with transaction.atomic():
            contract_invoice_obj = super(SupplierInvoiceSerializer, self).update(instance, validated_data)
            contract_invoice_obj.tenant = user.tenant
            contract_invoice_obj.utility = user.utility
            contract_invoice_obj.updated_by = user.id
            contract_invoice_obj.updated_date = timezone.now()
            contract_invoice_obj.save()
            return contract_invoice_obj