__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.jobcard import Jobcard as JobcardTbl


class JobcardShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobcardTbl
        fields = ('id_string', 'consumer_no')


# class JobcardViewSerializer(serializers.ModelSerializer):
#     tenant = TenantMasterViewSerializer(read_only=True)
#     utility = UtilityMasterViewSerializer(read_only=True)
#     supplier = SupplierShortViewSerializer(many=False, required=False, source='get_supplier')
#     due_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
#     created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
#     updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
#
#     class Meta:
#         model = JobcardTbl
#         fields = ('__all__')
#
#
# class JobcardSerializer(serializers.ModelSerializer):
#     contract = serializers.UUIDField(required=False)
#     supplier_financial = serializers.UUIDField(required=False)
#     demand = serializers.UUIDField(required=False)
#     invoice_no = serializers.CharField(required=True, max_length=500)
#     invoice_amount = serializers.FloatField(required=True)
#
#     class Meta:
#         model = JobcardTbl
#         fields = ('__all__')
#
#     def create(self, validated_data, supplier_obj, user):
#         validated_data = set_supplier_invoice_validated_data(validated_data)
#         if JobcardTbl.objects.filter(tenant=user.tenant, utility=user.utility,
#                                              supplier=supplier_obj.id, invoice_no=validated_data["invoice_no"]).exists():
#             return False
#         with transaction.atomic():
#             supplier_invoice_obj = super(JobcardTbl, self).create(validated_data)
#             supplier_invoice_obj.tenant = user.tenant
#             supplier_invoice_obj.utility = user.utility
#             supplier_invoice_obj.supplier = supplier_obj.id
#             supplier_invoice_obj.created_by = user.id
#             supplier_invoice_obj.save()
#             return supplier_invoice_obj
#
#     def update(self, instance, validated_data, user):
#         validated_data = set_supplier_invoice_validated_data(validated_data)
#         with transaction.atomic():
#             supplier_invoice_obj = super(JobcardTbl, self).update(instance, validated_data)
#             supplier_invoice_obj.tenant = user.tenant
#             supplier_invoice_obj.utility = user.utility
#             supplier_invoice_obj.updated_by = user.id
#             supplier_invoice_obj.updated_date = timezone.now()
#             supplier_invoice_obj.save()
#             return supplier_invoice_obj