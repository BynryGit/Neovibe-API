from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from v1.consumer.models.consumer_master import ConsumerMaster
from v1.consumer.views.common_functions import set_consumer_validated_data, generate_consumer_no


class ConsumerListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerMaster
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_no', 'email_id', 'phone_mobile')


class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    billing_state = serializers.ReadOnlyField(source='get_state')
    billing_city = serializers.ReadOnlyField(source='get_city')
    billing_area = serializers.ReadOnlyField(source='get_area')
    billing_sub_area = serializers.ReadOnlyField(source='get_sub_area')
    premise = serializers.ReadOnlyField(source='get_premise')

    class Meta:
        model = ConsumerMaster
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_no',
                  'master_consumer_no', 'email_id', 'phone_mobile', 'billing_address_line_1', 'billing_street',
                  'billing_zipcode', 'billing_state', 'billing_city', 'billing_area', 'billing_sub_area', 'premise')


class ConsumerSerializer(serializers.ModelSerializer):
    utility = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=True, max_length=200)
    billing_state_id = serializers.CharField(required=False, max_length=200)
    billing_city_id = serializers.CharField(required=False, max_length=200)
    billing_area_id = serializers.CharField(required=False, max_length=200)
    billing_sub_area_id = serializers.CharField(required=False, max_length=200)
    premise_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerMaster
        validators = [UniqueTogetherValidator(queryset=ConsumerMaster.objects.all(), fields=('phone_mobile',),
                                              message='Consumer already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_consumer_validated_data(validated_data)
        with transaction.atomic():
            consumer_obj = super(ConsumerSerializer, self).create(validated_data)
            consumer_obj.tenant = user.tenant
            consumer_obj.consumer_no = 111111
            # consumer_obj.consumer_no = generate_consumer_no(consumer_obj)
            consumer_obj.save()
            return consumer_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_validated_data(validated_data)
        with transaction.atomic():
            consumer_obj = super(ConsumerSerializer, self).update(instance, validated_data)
            return consumer_obj
