from rest_framework import serializers
from v1.registration.models.registrations import Registration


class RegistrationListSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = Registration
        fields = ('id_string', 'registration_no', 'first_name', 'last_name', 'email_id', 'phone_mobile', 'address_line_1',
                  'street', 'zipcode', 'status')