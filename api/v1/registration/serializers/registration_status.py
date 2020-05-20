from rest_framework import serializers
from v1.registration.models.registration_status import RegistrationStatus


class RegistrationStatusViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrationStatus
        fields = ('name','id_string')


