__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.meter_status import MeterStatusShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.consumer.models.consumer_master import get_consumer_by_consumer_no
from v1.meter_data_management.models.meter import get_meter_by_number
from v1.meter_data_management.models.meter_make import get_meter_make_by_id
from v1.meter_data_management.models.new_consumer_detail import NewConsumerDetail as NewConsumerDetailTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.reader_status import ReaderStatusListSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.serializers.schedule_log import ScheduleLogShortViewSerializer
from v1.meter_data_management.views.common_function import set_new_consumer_validated_data
from v1.userapp.serializers.user import UserShortViewSerializer


class NewConsumerDetailShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewConsumerDetailTbl
        fields = ('id_string', 'consumer_no', 'meter_no')


class NewConsumerDetailViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_log_id = ScheduleLogShortViewSerializer(many=False, source='get_schedule_log_name')
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    meter_reader_id = UserShortViewSerializer(many=False, source='get_meter_reader_name')
    meter_status_id = MeterStatusShortViewSerializer(many=False, source='get_meter_status_name')
    reader_status_id = ReaderStatusListSerializer(many=False, source='get_reader_status_name')
    meter_details = serializers.SerializerMethodField()
    consumer_details = serializers.SerializerMethodField()

    def get_meter_details(self, new_consumer_detail_tbl):
        meter_obj = get_meter_by_number(new_consumer_detail_tbl.meter_no)
        if meter_obj:
            meter_make_obj = get_meter_make_by_id(id=meter_obj.meter_make_id)
            meter_details = {
                'id_string': meter_obj.id_string,
                'device_no': meter_obj.device_no,
                'meter_no': meter_obj.meter_no,
                'meter_make': meter_make_obj.name,
                'meter_digit': meter_obj.meter_digit,
                'install_date': meter_obj.install_date,
            }
        else:
            meter_details = {
                'id_string': "NA",
                'device_no': "NA",
                'meter_no': "NA",
                'meter_make': "NA",
                'meter_digit': "NA",
                'install_date': "NA",
            }
        return meter_details

    def get_consumer_details(self, new_consumer_detail_tbl):
        consumer_master_obj = get_consumer_by_consumer_no(new_consumer_detail_tbl.consumer_no)
        if consumer_master_obj:
            consumer_details = {
                'first_name': consumer_master_obj.first_name,
                'last_name': consumer_master_obj.last_name,
                'email': consumer_master_obj.email,
                'phone_mobile': consumer_master_obj.phone_mobile,
            }
        else:
            consumer_details = {
                'first_name': "NA",
                'last_name': "NA",
                'email': "NA",
                'phone_mobile': "NA",
            }
        return consumer_details

    class Meta:
        model = NewConsumerDetailTbl
        fields = ('id_string', 'consumer_no', 'meter_no', 'current_meter_reading', 'created_date', 'meter_details',
                  'consumer_details', 'schedule_log_id', 'read_cycle_id', 'route_id', 'meter_reader_id',
                  'meter_status_id', 'reader_status_id', 'tenant', 'utility')


class NewConsumerDetailSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    schedule_log_id = serializers.UUIDField(required=True)
    read_cycle_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)
    consumer_no = serializers.CharField(max_length=50, required=True)
    meter_no = serializers.CharField(max_length=50, required=True)
    meter_status_id = serializers.UUIDField(required=False)
    reader_status_id = serializers.UUIDField(required=False)

    class Meta:
        model = NewConsumerDetailTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_new_consumer_validated_data(validated_data)
        try:
            new_consumer_obj = NewConsumerDetailTbl.objects.get(tenant=user.tenant,
                                                                utility_id=validated_data["utility_id"],
                                                                schedule_log_id=validated_data["schedule_log_id"],
                                                                read_cycle_id=validated_data["read_cycle_id"],
                                                                consumer_no= validated_data["consumer_no"],
                                                                meter_no= validated_data["meter_no"],
                                                                is_active=True)
            return new_consumer_obj
        except Exception:
            try:
                with transaction.atomic():
                    new_consumer_obj = super(NewConsumerDetailSerializer, self).create(validated_data)
                    new_consumer_obj.tenant = user.tenant
                    new_consumer_obj.meter_reader_id = user.id
                    new_consumer_obj.created_by = user.id
                    new_consumer_obj.save()
                    return new_consumer_obj
            except Exception as ex:
                print(ex)
                return None

    def update(self, instance, validated_data, user):
        validated_data = set_new_consumer_validated_data(validated_data)
        with transaction.atomic():
            new_consumer_obj = super(NewConsumerDetailSerializer, self).update(instance, validated_data)
            new_consumer_obj.updated_by = user.id
            new_consumer_obj.updated_date = timezone.now()
            new_consumer_obj.save()
            return new_consumer_obj
