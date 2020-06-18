__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_reading.models.meter_reading import MeterReading
from v1.meter_reading.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.meter_reading.serializers.meter_reading import MeterReadingShortViewSerializer
from v1.meter_reading.serializers.route import RouteShortViewSerializer
from v1.meter_reading.views.common_functions import set_validation_validated_data
from v1.userapp.serializers.user import UserViewSerializer
from v1.meter_reading.models.validation import Validation as ValidationTbl


class ValidationViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, required=False, source='get_bill_cycle')
    route_id = RouteShortViewSerializer(many=False, required=False, source='get_route')
    meter_reading_id = MeterReadingShortViewSerializer(many=False, required=False, source='get_meter_reading')
    validator_id = UserViewSerializer(many=False, required=False, source='get_validator')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = ValidationTbl
        fields = ('__all__')


class ValidationSerializer(serializers.ModelSerializer):
    bill_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)
    meter_reading_id = serializers.UUIDField(required=True)
    validator_id = serializers.UUIDField(required=True)
    is_meter_matching = serializers.BooleanField(required=True)
    is_reading_matching = serializers.BooleanField(required=True)

    class Meta:
        model = ValidationTbl
        fields = ('__all__')

    def update(self, instance, validated_data, user):
        validated_data = set_validation_validated_data(validated_data)
        with transaction.atomic():
            validation_obj = super(ValidationSerializer, self).update(instance, validated_data)
            validation_obj.tenant = user.tenant
            validation_obj.utility_id = 1
            validation_obj.updated_by = user.id
            validation_obj.updated_date = timezone.now()
            validation_obj.save()

            meter_reading_obj = MeterReading.objects.get(id=validation_obj.id)
            meter_reading_obj.reading_status_id = 2
            meter_reading_obj.save()
            return validation_obj
