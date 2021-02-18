__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.consumer.serializers.consumer_master import ConsumerViewSerializer
from v1.meter_data_management.models.consumer_meter import ConsumerMeter as ConsumerMeterTbl
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.serializers.meter import MeterViewSerializer


class ConsumerMeterViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    consumer_id = ConsumerViewSerializer(many=False, source='get_consumer_number')
    meter_id = MeterViewSerializer(many=False, source='get_meter_number')
    consumer_meter_status = ChoiceField(choices=ConsumerMeterTbl.CONSUMER_METER_STATUS)

    class Meta:
        model = ConsumerMeterTbl
        fields = ('id_string', 'consumer_meter_status', 'created_date', 'updated_date', 'created_by', 'updated_by',
                  'consumer_id', 'meter_id', 'tenant', 'utility')
