__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_payment import SupplierPayment as SupplierPaymentTbl
from v1.supplier.serializers.supplier import SupplierShortViewSerializer
from v1.supplier.views.common_functions import set_supplier_payment_validated_data


class SupplierPaymentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    supplier = SupplierShortViewSerializer(many=False, required=False, source='get_supplier')
    cheque_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    dd_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    payment_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = SupplierPaymentTbl
        fields = ('id_string', 'invoice_amount', 'paid_amount', 'cheque_no', 'dd_no', 'cheque_date', 'dd_date',
                  'payment_date', 'created_date', 'updated_date', 'bank_name', 'txn_id', 'account_no',
                  'ifsc_code', 'payment_source', 'tenant', 'utility', 'payment_type', 'invoice', 'contract', 'supplier',
                  'supplier_financial', 'demand')


class SupplierPaymentSerializer(serializers.ModelSerializer):
    invoice = serializers.UUIDField(required=False)
    contract = serializers.UUIDField(required=False)
    supplier_financial = serializers.UUIDField(required=False)
    demand = serializers.UUIDField(required=False)
    invoice_amount = serializers.FloatField(required=True)
    paid_amount = serializers.FloatField(required=True)
    cheque_no = serializers.IntegerField(required=False)
    dd_no = serializers.IntegerField(required=False)
    txn_id = serializers.IntegerField(required=True)
    bank_name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = SupplierPaymentTbl
        fields = ('__all__')

    def create(self, validated_data, supplier_obj, user):
        validated_data = set_supplier_payment_validated_data(validated_data)
        if SupplierPaymentTbl.objects.filter(tenant=user.tenant, utility=user.utility,
                                             supplier=supplier_obj.id, txn_id=validated_data["txn_id"]).exists():
            return False
        with transaction.atomic():
            supplier_payment_obj = super(SupplierPaymentSerializer, self).create(validated_data)
            supplier_payment_obj.tenant = user.tenant
            supplier_payment_obj.utility = user.utility
            supplier_payment_obj.supplier = supplier_obj.id
            supplier_payment_obj.created_by = user.id
            supplier_payment_obj.save()
            return supplier_payment_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_payment_validated_data(validated_data)
        with transaction.atomic():
            supplier_payment_obj = super(SupplierPaymentSerializer, self).update(instance, validated_data)
            supplier_payment_obj.tenant = user.tenant
            supplier_payment_obj.utility = user.utility
            supplier_payment_obj.updated_by = user.id
            supplier_payment_obj.updated_date = timezone.now()
            supplier_payment_obj.save()
            return supplier_payment_obj