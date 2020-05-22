__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_payment import SupplierPayment as SupplierPaymentTbl
from v1.supplier.views.common_functions import set_supplier_payment_validated_data


class SupplierPaymentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = SupplierPaymentTbl
        fields = ('__all__')


class SupplierPaymentSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant')
    utility = serializers.UUIDField(required=True, source='utility')
    invoice = serializers.IntegerField(required=False)
    contract = serializers.IntegerField(required=False)
    supplier = serializers.IntegerField(required=False)
    supplier_financial = serializers.IntegerField(required=False)
    demand = serializers.IntegerField(required=False)
    invoice_amount = serializers.FloatField(required=True)
    paid_amount = serializers.FloatField(required=True)
    invoice_date = serializers.DateTimeField(required=True)
    cheque_no = serializers.IntegerField(required=True)
    dd_no = serializers.IntegerField(required=True)
    bank_name = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = SupplierPaymentTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_supplier_payment_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierPaymentSerializer, self).create(validated_data)
            utility_obj.created_by = user.id
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_payment_validated_data(validated_data)
        with transaction.atomic():
            utility_obj = super(SupplierPaymentSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.save()
            return utility_obj