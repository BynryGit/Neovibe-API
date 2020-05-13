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