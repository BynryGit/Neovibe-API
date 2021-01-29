__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from api.messages import NAME_ALREADY_EXIST
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.serializers.tenant_city import TenantCitySerializer
from v1.tenant.serializers.tenant_country import TenantCountrySerializer
from v1.tenant.serializers.tenant_state import TenantStateSerializer
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.tenant.views.common_functions import set_tenant_validated_data


class TenantMasterViewSerializer(serializers.ModelSerializer):
    # tenant_country_id = TenantCountrySerializer(many=False, required=False, source='get_tenant_country')
    # tenant_state_id = TenantStateSerializer(many=False, required=False, source='get_tenant_state')
    # tenant_city_id = TenantCitySerializer(many=False, required=False, source='get_tenant_city')
    # status_id = TenantStatusViewSerializer(many=False, required=False, source='get_tenant_status')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = TenantMaster
        fields = ('__all__')


class TenantMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    email_id = serializers.CharField(required=True, max_length=200)
    tenant_country_id = serializers.UUIDField(required=True)
    tenant_state_id = serializers.UUIDField(required=True)
    tenant_city_id = serializers.UUIDField(required=True)
    status_id = serializers.UUIDField(required=True)

    class Meta:
        model = TenantMaster
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_tenant_validated_data(validated_data)
        if TenantMaster.objects.filter(name=validated_data["name"]).exists():
            raise CustomAPIException(NAME_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_obj = super(TenantMasterSerializer, self).create(validated_data)
            tenant_obj.created_by = user.id
            tenant_obj.save()
            return tenant_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tenant_validated_data(validated_data)
        with transaction.atomic():
            tenant_obj = super(TenantMasterSerializer, self).update(instance, validated_data)
            tenant_obj.updated_by = user.id
            tenant_obj.updated_date = timezone.now()
            tenant_obj.save()
            return tenant_obj
