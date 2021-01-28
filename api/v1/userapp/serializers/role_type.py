__author__ = "Arpita"

from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.role_type import RoleType
from v1.utility.serializers.utility import UtilitySerializer


class GetRoleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleType
        fields = ('__all__')


class RoleTypeListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = RoleType
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'updated_date')


class RoleTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = RoleType
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'updated_date')


class RoleTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = RoleType
        validators = [UniqueTogetherValidator(queryset=RoleType.objects.all(), fields=('name',), message='Role Type already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            type_obj = super(RoleTypeSerializer, self).create(validated_data)
            type_obj.created_by = user.id
            type_obj.updated_by = user.id
            type_obj.created_date = datetime.utcnow()
            type_obj.updated_date = datetime.utcnow()
            type_obj.tenant = user.tenant
            type_obj.utility = user.utility
            type_obj.is_active = True
            type_obj.save()
            return type_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            type_obj = super(RoleTypeSerializer, self).update(instance, validated_data)
            type_obj.updated_by = user.id
            type_obj.updated_date = datetime.utcnow()
            type_obj.is_active = True
            type_obj.save()
            return type_obj
