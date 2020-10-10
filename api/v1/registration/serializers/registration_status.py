from rest_framework import serializers
from v1.registration.models.registration_status import RegistrationStatus
from v1.registration.models.registrations import Registration



class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

class RegistrationStatusListSerializer(serializers.ModelSerializer):
    state = ChoiceField(choices=Registration.CHOICES)

    class Meta:
        model = RegistrationStatus
        fields = ('name','id_string', 'state', 'ui_class')


