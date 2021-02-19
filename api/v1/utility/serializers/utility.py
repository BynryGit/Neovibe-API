__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl
from v1.utility.views.common_functions import set_utility_validated_data, generate_company_id
from api.messages import UTILITY_WITH_GIVEN_DETAILS_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException


class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityMasterTbl
        fields = ('name', 'id_string')


class UtilityMasterViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UtilityMasterTbl
        fields = (
            'id_string', 'short_name', 'name', 'address', 'company_id', 'pan_no', 'tax_id', 'phone_no', 'email_id',
            'created_date', 'updated_date', 'tenant')


class UtilityMasterSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=True, source='tenant.id_string')
    short_name = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    phone_no = serializers.CharField(required=False, max_length=200)
    email_id = serializers.CharField(required=False, max_length=200)
    company_id = serializers.CharField(required=False, max_length=200)
    pan_no = serializers.CharField(required=False, max_length=200)
    tax_id = serializers.CharField(required=True, max_length=200,
                                   error_messages={"required": "The field Tax ID is required."})
    address = serializers.CharField(required=False, max_length=200)
    region_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField(required=False)
    state_id = serializers.IntegerField(required=False)
    city_id = serializers.IntegerField(required=False)
    status_id = serializers.IntegerField(required=False)

    class Meta:
        model = UtilityMasterTbl
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_utility_validated_data(validated_data)
        if UtilityMasterTbl.objects.filter(tenant=validated_data["tenant"], name=validated_data["name"],
                                           tax_id=validated_data['tax_id']).exists():
            raise CustomAPIException(UTILITY_WITH_GIVEN_DETAILS_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                if 'tenant' in validated_data:
                    tenant = validated_data.pop('tenant')
                utility_obj = super(UtilityMasterSerializer, self).create(validated_data)
                utility_obj.created_by = user.id
                utility_obj.created_date = timezone.now()
                utility_obj.tenant_id = tenant
                utility_obj.company_id = generate_company_id(utility_obj)
                utility_obj.save()
                return utility_obj

    def update(self, instance, validated_data, user):
        validated_data = set_utility_validated_data(validated_data)
        with transaction.atomic():
            if 'tenant' in validated_data:
                tenant = validated_data.pop('tenant')
            utility_obj = super(UtilityMasterSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user.id
            utility_obj.updated_date = timezone.now()
            utility_obj.tenant_id = tenant
            utility_obj.save()
            return utility_obj
