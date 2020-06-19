__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.meter_reading import MeterReading
from v1.meter_reading.models.route_upload import RouteUpload as RouteUploadTbl
from v1.meter_reading.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_reading.serializers.route import RouteShortViewSerializer
from v1.meter_reading.serializers.route_upload_status import RouteUploadStatusShortViewSerializer
from v1.meter_reading.views.common_functions import set_route_upload_validated_data


class RouteUploadViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, required=False, source='get_bill_cycle')
    route_id = RouteShortViewSerializer(many=False, required=False, source='get_route')
    route_upload_status_id = RouteUploadStatusShortViewSerializer(many=False, required=False, source='get_route_upload_status')
    upload_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = RouteUploadTbl
        fields = ('__all__')


class RouteUploadSerializer(serializers.ModelSerializer):
    bill_cycle_id = serializers.UUIDField(required=True)
    month = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = RouteUploadTbl
        fields = ('__all__')

    def create(self, validated_data, route_obj, user):
        validated_data = set_route_upload_validated_data(validated_data)
        if RouteUploadTbl.objects.filter(tenant=user.tenant, utility=1, bill_cycle_id=validated_data["bill_cycle_id"],
                                         route_id=route_obj.id, month=validated_data["month"]).exists():
            return False
        with transaction.atomic():
            route_upload_obj = super(RouteUploadSerializer, self).create(validated_data)
            route_upload_obj.tenant = user.tenant
            route_upload_obj.utility_id = 1
            route_upload_obj.token = route_obj.token
            route_upload_obj.created_by = user.id
            route_upload_obj.save()

            meter_reading_obj = MeterReading.objects.filter(month=validated_data["month"], route_id=route_obj.id,
                                                       bill_cycle_id=validated_data["bill_cycle_id"])

            # Todo code for send reading

            route_upload_obj.route_upload_status_id=2
            route_upload_obj.save()
            return route_upload_obj
