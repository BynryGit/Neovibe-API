__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.consumer import Consumer as ConsumerTbl


class ConsumerShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerTbl
        fields = ('id_string', 'consumer_no')


class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ConsumerTbl
        fields = ('__all__')