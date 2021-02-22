__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.meter_make import MeterMake as MeterMakeTbl


class MeterMakeShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterMakeTbl
        fields = ('id_string', 'name')


class MeterMakeViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = MeterMakeTbl
        fields = ('__all__')
