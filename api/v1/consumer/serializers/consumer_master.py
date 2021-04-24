from datetime import datetime
from django.db import transaction
from rest_framework import serializers, status
from api.messages import MOBILE_ALREADY_EXISTS
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_master import ConsumerMaster
# from v1.consumer.views.common_functions import set_consumer_validated_data, generate_consumer_no
from v1.consumer.views.common_functions import *
from v1.consumer.views import common_functions


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


class ConsumerListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerMaster
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_no', 'email',
                  'phone_mobile','billing_address_line_1')


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
    account_type = ChoiceField(choices=ConsumerMaster.ACCOUNT_TYPE)

    class Meta:
        model = ConsumerMaster
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'consumer_no',
                  'master_consumer_no', 'email', 'phone_mobile', 'billing_address_line_1', 'billing_street',
                  'billing_zipcode', 'billing_state', 'billing_city', 'billing_area', 'billing_sub_area', 'premise',
                  'account_type')


class ConsumerSerializer(serializers.ModelSerializer):
    utility = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=True, max_length=200)
    billing_state_id = serializers.CharField(required=False, max_length=200)
    billing_city_id = serializers.CharField(required=False, max_length=200)
    billing_area_id = serializers.CharField(required=False, max_length=200)
    billing_sub_area_id = serializers.CharField(required=False, max_length=200)
    ownership_id = serializers.CharField(required=False, max_length=200)
    premise_id = serializers.CharField(required=False, max_length=200)
    # credit_rating_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerMaster
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = common_functions.set_consumer_validated_data(validated_data)
        if ConsumerMaster.objects.filter(phone_mobile=validated_data['phone_mobile'],
                                         utility_id=validated_data['utility']).exists():
            raise CustomAPIException(MOBILE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                consumer_obj = super(ConsumerSerializer, self).create(validated_data)
                consumer_obj.tenant = user.tenant
                consumer_obj.created_by = user.id
                consumer_obj.created_date = datetime.now()
                consumer_obj.consumer_no = common_functions.generate_consumer_no(consumer_obj)
                consumer_obj.is_active = True
                consumer_obj.save()
                return consumer_obj

    def update(self, instance, validated_data, user):
        validated_data = common_functions.set_consumer_validated_data(validated_data)
        if ConsumerMaster.objects.exclude(id_string=instance.id_string).filter(
                phone_mobile=validated_data['phone_mobile'], utility=instance.utility).exists():
            raise CustomAPIException(MOBILE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                consumer_obj = super(ConsumerSerializer, self).update(instance, validated_data)
                return consumer_obj
