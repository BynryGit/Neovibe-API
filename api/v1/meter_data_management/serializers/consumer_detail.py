__author__ = "aki"

from rest_framework import serializers
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl


class ConsumerDetailShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerDetailTbl
        fields = ('id_string', 'consumer_no', 'meter_no')
