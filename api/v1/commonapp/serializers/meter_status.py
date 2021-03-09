__author__ = "chinmay"

from rest_framework import serializers
from v1.commonapp.models.meter_status import MeterStatus as MeterStatusTbl


class MeterStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterStatusTbl
        fields = ('name', 'status_code', 'id_string', 'is_active', 'created_by', 'created_date')
