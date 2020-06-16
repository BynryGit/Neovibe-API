__author__ = "aki"

from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.meter_reading_images import MeterImage as MeterImageTbl


class MeterImageSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    meter_image_url = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    def get_meter_image_url(self, meter_image_tbl):
        request = self.context.get('request')
        if meter_image_tbl.meter_image:
            meter_image_url = request.build_absolute_uri(meter_image_tbl.meter_image.url)
        else:
            meter_image_url=''
        return meter_image_url

    class Meta:
        model = MeterImageTbl
        fields = ('id_string', 'consumer_no', 'meter_image', 'meter_image_url', 'type_id', 'meter_reading_id',
                  'tenant', 'utility')

    def create(self, validated_data, user):
        meter_image = super(MeterImageSerializer, self).create(validated_data)
        meter_image.created_by = user
        meter_image.save()
        return meter_image
