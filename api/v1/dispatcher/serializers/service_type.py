from rest_framework import serializers
from v1.dispatcher.models.service_type import ServiceTypes
from api.settings import DISPLAY_DATE_TIME_FORMAT

class ServiceTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTypes
        fields = ('name','id_string')

