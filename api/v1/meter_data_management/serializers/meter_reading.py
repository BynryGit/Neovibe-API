__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from api.messages import METER_READING_ALREADY_EXIST
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.serializers.consumer_detail import ConsumerDetailShortViewSerializer
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer
from v1.meter_data_management.serializers.route_task_assignment import RouteTaskAssignmentShortViewSerializer


class MeterReadingShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterReadingTbl
        fields = ('id_string', 'consumer_no', 'meter_no')


class MeterReadingViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    consumer_detail_id = ConsumerDetailShortViewSerializer(many=False, source='get_consumer_detail')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    route_task_assignment_id = RouteTaskAssignmentShortViewSerializer(many=False, source='get_route_task_assignmnet')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_name')
    # meter_reader_id = (many=False, source='get_meter_reader_name')
    # validator_one_id = (many=False, source='get_validator_one_name')
    # validator_two_id = (many=False, source='get_validator_two_name')
    reading_status = ChoiceField(choices=MeterReadingTbl.READING_STATUS)

    def get_meter_image_url(self, meter_reading_tbl):
        request = self.context.get('request')
        if meter_reading_tbl.meter_image:
            meter_image_url = request.build_absolute_uri(meter_reading_tbl.meter_image.url)
        else:
            meter_image_url = ''
        return meter_image_url

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')


class MeterReadingSerializer(serializers.ModelSerializer):
    read_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        # validated_data = set_meter_reading_validated_data(validated_data)
        if MeterReadingTbl.objects.filter(tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException(METER_READING_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            meter_reading_obj = super(MeterReadingSerializer, self).create(validated_data)
            meter_reading_obj.tenant = user.tenant
            meter_reading_obj.created_by = user.id
            meter_reading_obj.save()
            return meter_reading_obj

    def update(self, instance, validated_data, user):
        # validated_data = set_meter_reading_validated_data(validated_data)
        with transaction.atomic():
            meter_reading_obj = super(MeterReadingSerializer, self).update(instance, validated_data)
            meter_reading_obj.tenant = user.tenant
            meter_reading_obj.updated_by = user.id
            meter_reading_obj.updated_date = timezone.now()
            meter_reading_obj.save()
            return meter_reading_obj