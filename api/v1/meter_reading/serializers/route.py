__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.route import Route as RouteTbl


class RouteShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'name')


class RouteViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'code', 'name', 'created_date', 'updated_date', 'tenant', 'utility', 'city', 'area',
                  'subarea')