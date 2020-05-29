__author__ = "Arpita"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.service_type import ServiceType


class ServiceTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('name', 'id_string')

class ServiceTypeViewSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    created_date = serializers.SerializerMethodField('get_created_date')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = ServiceType
        fields = ('id_string', 'tenant_name', 'name','created_date','is_active')