from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.country import CountrySerializer
from v1.commonapp.serializers.state import StateSerializer
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_status import TenantStatus
from v1.tenant.views.common_functions import set_validated_data


class GetTenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantStatus
        fields = ('name','id_string')


class TenantStatusViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantStatus
        fields = ('name','id_string')


class TenantMasterViewSerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()
    state_id = StateSerializer()
    city_id = CitySerializer()
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantMaster
        fields = ('id_string', 'short_name', 'name', 'email_id', 'mobile_no', 'created_date', 'updated_date', 'status_id',
                  'country_id', 'state_id', 'city_id')


class TenantMasterSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=False, max_length=200)
    email_id = serializers.CharField(required=False, max_length=200)
    mobile_no = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    country_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantMaster
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_validated_data(validated_data)
        if TenantMaster.objects.filter(**validated_data).exists():
            return False
        with transaction.atomic():
            tenant_obj = super(TenantMasterSerializer, self).create(validated_data)
            tenant_obj.created_by = user.id
            tenant_obj.save()
            return tenant_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_obj = super(TenantMasterSerializer, self).update(instance, validated_data)
            tenant_obj.updated_by = user.id
            tenant_obj.updated_date = timezone.now()
            tenant_obj.save()
            return tenant_obj