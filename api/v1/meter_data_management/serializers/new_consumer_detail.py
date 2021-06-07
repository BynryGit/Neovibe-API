__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.models.new_consumer_detail import NewConsumerDetail as NewConsumerDetailTbl
from v1.meter_data_management.serializers.read_cycle import ReadCycleShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.views.common_function import set_new_consumer_validated_data
from v1.userapp.serializers.user import UserShortViewSerializer


class NewConsumerDetailShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewConsumerDetailTbl
        fields = ('id_string', 'consumer_no', 'meter_no')


class NewConsumerDetailViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    read_cycle_id = ReadCycleShortViewSerializer(many=False, source='get_read_cycle_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    meter_reader_id = UserShortViewSerializer(many=False, source='get_meter_reader_name')

    class Meta:
        model = NewConsumerDetailTbl
        fields = ('__all__')


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
