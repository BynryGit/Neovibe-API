from django.db import transaction
from rest_framework import serializers
from v1.billing.models.invoice_bill import InvoiceBill
from v1.billing.views.common_functions import set_validated_data
from v1.consumer.serializers.consumer_category import ConsumerCategoryListSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryListSerializer


class InvoiceBillListSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceBill
        fields = ('id_string', 'invoice_no', 'invoice_date', 'consumer_no', 'bill_month', 'due_date', 'before_due_date_amount',
                  'after_due_date_amount')

class InvoiceBillViewSerializer(serializers.ModelSerializer):
    category = ConsumerCategoryListSerializer(many=False, source='get_category')
    sub_category = ConsumerSubCategoryListSerializer(many=False, source='get_sub_category')

    class Meta:
        model = InvoiceBill
        fields = ('__all__')


class InvoiceBillSerializer(serializers.ModelSerializer):
    consumer_no = serializers.CharField(required=True, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    cycle_id = serializers.CharField(required=False, max_length=200)
    route_id = serializers.CharField(required=False, max_length=200)
    utility_service_plan_id = serializers.CharField(required=False, max_length=200)
    bill_status_id = serializers.CharField(required=False, max_length=200)
    instruction_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = InvoiceBill
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            invoice_bill_obj = super(InvoiceBillSerializer, self).create(validated_data)
            return invoice_bill_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            invoice_bill_obj = super(InvoiceBillSerializer, self).update(instance, validated_data)
            return invoice_bill_obj