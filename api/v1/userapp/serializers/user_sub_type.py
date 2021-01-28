__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_sub_type import UserSubType
from v1.userapp.serializers.user_type import GetUserTypeSerializer
from v1.userapp.views.common_functions import set_user_sub_type_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class GetUserSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubType
        fields = ('name', 'id_string','key')


class UserSubTypeListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user_type = GetUserTypeSerializer(many=False, required=True, source='get_role_type')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UserSubType
        fields = ('id_string', 'tenant', 'utility', 'user_type', 'name', 'created_date', 'updated_date')


class UserSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user_type = GetUserTypeSerializer(many=False, required=True, source='get_role_type')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UserSubType
        fields = ('id_string', 'tenant', 'utility', 'user_type', 'name', 'created_date', 'updated_date')


class UserSubTypeSerializer(serializers.ModelSerializer):
    user_type_id = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserSubType
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_sub_type_validated_data(validated_data)
        with transaction.atomic():
            sub_type_obj = super(UserSubTypeSerializer, self).create(validated_data)
            sub_type_obj.created_by = user.id
            sub_type_obj.updated_by = user.id
            sub_type_obj.created_date = datetime.utcnow()
            sub_type_obj.updated_date = datetime.utcnow()
            sub_type_obj.tenant = user.tenant
            sub_type_obj.utility = user.utility
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_user_sub_type_validated_data(validated_data)
        with transaction.atomic():
            sub_type_obj = super(UserSubTypeSerializer, self).update(instance, validated_data)
            sub_type_obj.updated_by = user.id
            sub_type_obj.updated_date = datetime.utcnow()
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj

