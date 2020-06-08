__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.tenant.serializers.tenant_city import TenantCitySerializer
from v1.tenant.serializers.tenant_country import TenantCountrySerializer
from v1.tenant.serializers.tenant_state import TenantStateSerializer
from v1.tender.models.tender import Tender as TenderTbl
from v1.tender.views.common_functions import set_tender_validated_data


class TenderShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenderTbl
        fields = ('id_string', 'name')


class TenderViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    country_id = TenantCountrySerializer(many=False, required=False, source='get_tenant_country')
    state_id = TenantStateSerializer(many=False, required=False, source='get_tenant_state')
    city_id = TenantCitySerializer(many=False, required=False, source='get_tenant_city')
    status_id = TenantCitySerializer(many=False, required=False, source='get_tenant_status')
    type_id = TenantCitySerializer(many=False, required=False, source='get_tenant_type')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenderTbl
        fields = ('id_string', 'tender_no', 'tender_name', 'description', 'start_date', 'end_date', 'pre_bidding_date',
                  'submission_date', 'due_date', 'eic_name', 'eic_contact_no', 'amount', 'created_date', 'updated_date',
                  'type_id', 'status_id', 'tenant', 'utility', 'country_id', 'state_id', 'city_id')


class TenderSerializer(serializers.ModelSerializer):
    country_id = serializers.UUIDField(required=False)
    state_id = serializers.UUIDField(required=False)
    city_id = serializers.UUIDField(required=False)
    type_id = serializers.UUIDField(required=True)
    status_id = serializers.UUIDField(required=True)
    tender_no = serializers.CharField(required=True, max_length=200)
    tender_name = serializers.CharField(required=True, max_length=500)
    description = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = TenderTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_tender_validated_data(validated_data)
        if TenderTbl.objects.filter(tenant=user.tenant, utility=user.utility, name=validated_data["name"]).exists():
            return False
        with transaction.atomic():
            tender_obj = super(TenderSerializer, self).create(validated_data)
            tender_obj.tenant = user.tenant
            tender_obj.utility = 1
            tender_obj.created_by = user.id
            tender_obj.save()
            return tender_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tender_validated_data(validated_data)
        with transaction.atomic():
            tender_obj = super(TenderSerializer, self).update(instance, validated_data)
            tender_obj.tenant = user.tenant
            tender_obj.utility = 1
            tender_obj.updated_by = user.id
            tender_obj.updated_date = timezone.now()
            tender_obj.save()
            return tender_obj