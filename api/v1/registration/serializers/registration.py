from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from v1.registration.models.registration_status import RegistrationStatus
from v1.registration.models.registrations import Registration


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
    status = RegistrationStatusViewSerializer(many=False,required=True,source='get_status')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = Registration
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'registration_no', 'status',
                  'first_name', 'last_name', 'email_id', 'phone_mobile', 'address_line_1', 'street', 'zipcode')


class RegistrationSerializer(serializers.ModelSerializer):
    tenant_id_string = serializers.UUIDField(required=True)
    utility_id_string = serializers.UUIDField(required=True)

    class Meta:
        model = Registration
        fields = (
        'tenant', 'utility', 'registration_no', 'status', 'first_name', 'last_name', 'email_id',
        'phone_mobile', 'address_line_1', 'street', 'zipcode')

    def create(self, validated_data, user):
        with transaction.atomic():
            payments = []
            if 'payments' in validated_data:
                payments = validated_data.pop('payments')

            registration_obj = super(RegistrationSerializer, self).create(validated_data)
            registration_obj.created_by = user
            registration_obj.created_date = datetime.now()
            registration_obj.save()
            for payment in payments:
                payment['identification'] = registration_obj.id
                payment_obj = PaymentSerializer(**payment)
            return registration_obj, payment_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            registration_obj = super(RegistrationSerializer, self).update(instance, validated_data)
            registration_obj.updated_by = user
            registration_obj.updated_date = datetime.now()
            registration_obj.save()
            return registration_obj