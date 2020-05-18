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