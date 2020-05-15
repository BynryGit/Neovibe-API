from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.serializers.area import AreaListSerializer
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id_string
from v1.payment.models.consumer_payment import get_payment_by_id_string
from v1.registration.models.registration_status import RegistrationStatus, get_registration_status_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.registration.models.registrations import Registration
from v1.registration.views.common_functions import set_validated_data


class RegistrationStatusViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrationStatus
        fields = ('name','id_string')


class RegistrationListSerializer(serializers.ModelSerializer):
    status = RegistrationStatusViewSerializer(many=False,required=True,source='get_status')

    class Meta:
        model = Registration
        fields = ('id_string', 'registration_no', 'first_name', 'last_name', 'email_id', 'phone_mobile', 'address_line_1',
                  'street', 'zipcode', 'status')


class RegistrationViewSerializer(serializers.ModelSerializer):
    status = RegistrationStatusViewSerializer(many=False, source='get_status')
    area = AreaListSerializer(many=False, source='get_area')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = Registration
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'registration_no', 'first_name',
                  'last_name', 'email_id', 'phone_mobile', 'address_line_1', 'street', 'zipcode', 'status', 'area')


class RegistrationSerializer(serializers.ModelSerializer):
    phone_mobile = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    registration_type_id = serializers.CharField(required=False, max_length=200)
    country_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    scheme_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    payment_id = serializers.CharField(required=False, max_length=200)
    ownership_id = serializers.CharField(required=False, max_length=200)
    consumer_category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    source_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Registration
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data =  set_validated_data(validated_data)
        with transaction.atomic():
            payments = []
            if 'payments' in validated_data:
                payments = validated_data.pop('payments')

            registration_obj = super(RegistrationSerializer, self).create(validated_data)
            registration_obj.created_by = user.id
            registration_obj.created_date = datetime.now()
            registration_obj.tenant = user.tenant
            registration_obj.utility = user.utility
            registration_obj.save()
            if payments:
                for payment in payments:
                    payment['identification'] = registration_obj.id
                    payment_obj = PaymentSerializer(**payment)
            return registration_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            payments = []
            if 'payments' in validated_data:
                payments = validated_data.pop('payments')

            registration_obj = super(RegistrationSerializer, self).update(instance, validated_data)
            registration_obj.updated_by = user
            registration_obj.updated_date = datetime.now()
            registration_obj.save()
            if payments:
                for payment in payments:
                    payment['identification'] = registration_obj.id
                    payment_obj = PaymentSerializer(**payment)
            return registration_obj