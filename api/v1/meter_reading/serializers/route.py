__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.route import Route as RouteTbl


class RouteShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTbl
        fields = ('name', 'id_string')


class RouteViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = RouteTbl
        fields = ('id_string', 'code', 'name', 'tenant', 'utility', 'city', 'area', 'subarea')