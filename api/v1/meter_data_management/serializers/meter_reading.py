__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_data_management.serializers.consumer import ConsumerShortViewSerializer
from v1.meter_data_management.serializers.job_card import JobcardShortViewSerializer
from v1.meter_data_management.serializers.meter_image_type import MeterImageTypeShortViewSerializer
from v1.meter_data_management.serializers.meter_status import MeterStatusShortViewSerializer
from v1.meter_data_management.serializers.reader_status import ReaderStatusShortViewSerializer
from v1.meter_data_management.serializers.reading_status import ReadingStatusShortViewSerializer
from v1.meter_data_management.serializers.reading_taken_by import ReadingTakenByShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.views.common_functions import set_meter_reading_validated_data


class MeterReadingShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterReadingTbl
        fields = ('id_string', 'consumer_no')


class MeterReadingViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle')
    route_id = RouteShortViewSerializer(many=False, source='get_route')
    jobcard_id = JobcardShortViewSerializer(many=False, source='get_jobcard')
    reading_status_id = ReadingStatusShortViewSerializer(many=False, source='get_reading_status')
    meter_status_id = MeterStatusShortViewSerializer(many=False, source='get_meter_status')
    reader_status_id = ReaderStatusShortViewSerializer(many=False, source='get_reader_status_id')
    reading_taken_by_id = ReadingTakenByShortViewSerializer(many=False, source='get_reading_taken_by')
    consumer_id = ConsumerShortViewSerializer(many=False, source='get_consumer')
    meter_image_type_id = MeterImageTypeShortViewSerializer(many=False, source='get_meter_image_type')
    meter_image_url = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    def get_meter_image_url(self, meter_reading_tbl):
        request = self.context.get('request')
        if meter_reading_tbl.meter_image:
            meter_image_url = request.build_absolute_uri(meter_reading_tbl.meter_image.url)
        else:
            meter_image_url = ''
        return meter_image_url

    class Meta:
        model = MeterReadingTbl
        fields = ('id_string', 'month', 'consumer_no', 'meter_no', 'meter_image_url', 'meter_image', 'current_reading',
                  'consumption', 'suspicious_activity', 'is_qr_tempered', 'is_solar_meter', 'is_duplicate', 'is_new',
                  'is_assign_to_v1', 'is_assign_to_v2', 'is_account_verified', 'reading_date', 'created_date',
                  'updated_date', 'meter_image_type_id', 'consumer_id', 'bill_cycle_id', 'route_id', 'jobcard_id',
                  'reading_status_id', 'meter_status_id', 'reader_status_id', 'reading_taken_by_id', 'tenant',
                  'utility')


class MeterReadingSerializer(serializers.ModelSerializer):
    bill_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)
    jobcard_id = serializers.UUIDField(required=True)
    reading_status_id = serializers.UUIDField(required=True)
    meter_status_id = serializers.UUIDField(required=True)
    reader_status_id = serializers.UUIDField(required=True)
    reading_taken_by_id = serializers.UUIDField(required=True)

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_meter_reading_validated_data(validated_data)
        if MeterReadingTbl.objects.filter(tenant=user.tenant, utility_id=1, route_id=validated_data["route_id"],
                                          bill_cycle_id=validated_data["bill_cycle_id"]).exists():
            return False
        with transaction.atomic():
            meter_reading_obj = super(MeterReadingSerializer, self).create(validated_data)
            meter_reading_obj.tenant = user.tenant
            meter_reading_obj.utility_id = 1
            meter_reading_obj.created_by = user.id
            meter_reading_obj.save()
            return meter_reading_obj

    def update(self, instance, validated_data, user):
        validated_data = set_meter_reading_validated_data(validated_data)
        with transaction.atomic():
            meter_reading_obj = super(MeterReadingSerializer, self).update(instance, validated_data)
            meter_reading_obj.tenant = user.tenant
            meter_reading_obj.utility_id = 1
            meter_reading_obj.updated_by = user.id
            meter_reading_obj.updated_date = timezone.now()
            meter_reading_obj.save()
            return meter_reading_obj
