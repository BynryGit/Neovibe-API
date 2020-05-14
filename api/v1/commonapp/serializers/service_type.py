__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.service_type import ServiceType


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('name', 'id_string')