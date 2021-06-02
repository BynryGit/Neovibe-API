__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.models.premises import get_premise_by_id
from v1.commonapp.serializers.area import AreaShortViewSerializer
from v1.commonapp.serializers.city import CityShortViewSerializer
from v1.commonapp.serializers.meter_status import MeterStatusShortViewSerializer
from v1.commonapp.serializers.premises import PremisesShortViewSerializer
from v1.commonapp.serializers.state import StateShortViewSerializer
from v1.commonapp.serializers.sub_area import SubAreaShortViewSerializer
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_meter_id
from v1.meter_data_management.models.meter import Meter as MeterTbl
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.meter_data_management.serializers.meter_make import MeterMakeShortViewSerializer
from v1.meter_data_management.serializers.route import RouteShortViewSerializer
from v1.meter_data_management.views.common_function import set_meter_validated_data
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import DATA_ALREADY_EXISTS
from v1.utility.views.common_functions import generate_meter_no


class MeterShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeterTbl
        fields = ('id_string', 'meter_make')


class MeterViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    state_id = StateShortViewSerializer(many=False, source='get_state_name')
    city_id = CityShortViewSerializer(many=False, source='get_city_name')
    area_id = AreaShortViewSerializer(many=False, source='get_area_name')
    sub_area_id = SubAreaShortViewSerializer(many=False, source='get_sub_area_name')
    route_id = RouteShortViewSerializer(many=False, source='get_route_name')
    premise_id = PremisesShortViewSerializer(many=False, source='get_premise_type')
    category_id = GlobalLookupShortViewSerializer(many=False, source='get_category_name')
    meter_type_id = GlobalLookupShortViewSerializer(many=False, source='get_meter_type_name')
    meter_make_id = MeterMakeShortViewSerializer(many=False, source='get_meter_make')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_name')
    meter_status = MeterStatusShortViewSerializer(many=False, source='get_meter_status_name')
    state = ChoiceField(choices=MeterTbl.STATE)
    consumer_detail = serializers.SerializerMethodField()

    def get_consumer_detail(self, meter_tbl):
        consumer_service_contract_obj = get_consumer_service_contract_detail_by_meter_id(meter_tbl.id)
        if consumer_service_contract_obj:
            consumer_master_obj = get_consumer_by_id(consumer_service_contract_obj.consumer_id)
            if consumer_master_obj:
                consumer_detail = {
                    "id": consumer_master_obj.id_string,
                    "consumer_number": consumer_master_obj.consumer_no
                }
            else:
                consumer_detail = {
                    "consumer_number": "Na"
                }
        else:
            consumer_detail = {
                "consumer_number": "Na"
            }

        return consumer_detail

    class Meta:
        model = MeterTbl
        fields = ('id_string', 'device_no', 'meter_no', 'state', 'meter_digit', 'current_reading', 'latitude',
                  'longitude', 'consumer_detail', 'meter_status', 'reader_status', 'install_date', 'created_by',
                  'updated_by', 'created_date', 'updated_date', 'state_id', 'city_id', 'area_id', 'sub_area_id',
                  'route_id', 'premise_id', 'meter_type_id', 'meter_make_id', 'utility_product_id', 'category_id',
                  'tenant', 'utility',)


class MeterSerializer(serializers.ModelSerializer):
    device_no = serializers.CharField(required=True)
    utility_id = serializers.UUIDField(required=True)
    route_id = serializers.UUIDField(required=True)
    premise_id = serializers.UUIDField(required=True)
    meter_type_id = serializers.UUIDField(required=False)
    meter_make_id = serializers.UUIDField(required=False)
    meter_status = serializers.UUIDField(required=False)
    utility_product_id = serializers.UUIDField(required=False)
    meter_detail = serializers.JSONField(required=False)
    meter_no = serializers.CharField(required=False)

    class Meta:
        model = MeterTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_meter_validated_data(validated_data)
        if MeterTbl.objects.filter(tenant=user.tenant, utility_id=validated_data['utility_id'],
                                   device_no=validated_data['device_no'], is_active=True).exists():
            raise CustomAPIException(DATA_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                meter_obj = super(MeterSerializer, self).create(validated_data)
                meter_obj.tenant = user.tenant
                meter_obj.created_by = user.id
                meter_obj.save()
                premise_obj = get_premise_by_id(meter_obj.premise_id)
                meter_obj.state_id = premise_obj.state_id
                meter_obj.city_id = premise_obj.city_id
                meter_obj.area_id = premise_obj.area_id
                meter_obj.meter_no = generate_meter_no(meter_obj.tenant.id)
                meter_obj.save()
                return meter_obj

    def update(self, instance, validated_data, user):
        validated_data = set_meter_validated_data(validated_data)
        with transaction.atomic():
            meter_obj = super(MeterSerializer, self).update(instance, validated_data)
            meter_obj.tenant = user.tenant
            meter_obj.updated_by = user.id
            meter_obj.updated_date = timezone.now()
            meter_obj.save()
            return meter_obj
