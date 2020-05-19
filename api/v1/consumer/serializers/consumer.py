from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_master import ConsumerMaster
from v1.consumer.views.common_functions import set_validated_data


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


class ConsumerSerializer(serializers.ModelSerializer):
    country_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    cycle_id = serializers.CharField(required=False, max_length=200)
    route_id = serializers.CharField(required=False, max_length=200)
    scheme_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    utility_service_plan_id = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    consumer_status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerMaster
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data =  set_validated_data(validated_data)
        with transaction.atomic():
            consumer_obj = super(ConsumerSerializer, self).create(validated_data)
            return consumer_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            consumer_obj = super(ConsumerSerializer, self).update(instance, validated_data)
            return consumer_obj