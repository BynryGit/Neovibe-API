__author__ = "Priyanka"

from api.settings import DISPLAY_DATE_TIME_FORMAT
from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.dispatcher.models.sop_master import SopMaster
from v1.commonapp.serializers.service_type import ServiceTypeListSerializer
from v1.commonapp.serializers.city import CitySerializer


class SOPViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    def get_effective_start_date(self, obj):
        return obj.effective_start_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    def get_effective_end_date(self, obj):
        return obj.effective_end_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    service_type_id = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    city_id = CitySerializer(many=False, required=True, source='get_city')
    created_date = serializers.SerializerMethodField('get_created_date')
    effective_start_date = serializers.SerializerMethodField('get_effective_start_date')
    effective_end_date = serializers.SerializerMethodField('get_effective_end_date')
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = SopMaster
        fields = ('id_string', 'tenant_name', 'name','effective_start_date','effective_end_date','service_type_id','city_id','created_date',
                  'is_active')

