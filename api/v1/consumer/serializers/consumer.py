from rest_framework import serializers

from v1.billing.models.invoice_bill import InvoiceBill
from v1.consumer.models.consumer_master import ConsumerMaster


class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerMaster
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_no', 'first_name',
                  'middle_name', 'last_name', 'email_id', 'phone_mobile', 'phone_landline', 'address_line_1', 'street', 'zipcode',
                  'deposit_amt', 'collected_amt', 'registration', 'is_vip', 'is_connectivity', 'gas_demand', 'monthly_demand',
                  'consumption_ltd', 'invoice_amount_ltd', 'payment_ltd', 'outstanding_ltd', 'is_active', 'created_date', 'updated_date',
                  )


class ConsumerBillListSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceBill
        fields = ('id_string', 'bill_month', 'before_due_date_amount', 'due_date', 'bill_status')