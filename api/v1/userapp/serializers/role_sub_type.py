__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.role_sub_type import RoleSubType
from v1.userapp.serializers.role_type import GetRoleTypeSerializer
from v1.userapp.views.common_functions import set_role_sub_type_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class GetRoleSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleSubType
        fields = ('name', 'id_string')


class RoleSubTypeListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role_type = GetRoleTypeSerializer(many=False, required=True, source='get_role_type')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = RoleSubType
        fields = ('id_string', 'tenant', 'utility', 'role_type', 'name', 'created_date', 'updated_date')


class RoleSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role_type = GetRoleTypeSerializer(many=False, required=True, source='get_role_type')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = RoleSubType
        fields = ('id_string', 'tenant', 'utility', 'role_type', 'name', 'created_date', 'updated_date')


class RoleSubTypeSerializer(serializers.ModelSerializer):
    role_type_id = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = RoleSubType
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_role_sub_type_validated_data(validated_data)
        with transaction.atomic():
            sub_type_obj = super(RoleSubTypeSerializer, self).create(validated_data)
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
        validated_data = set_role_sub_type_validated_data(validated_data)
        with transaction.atomic():
            sub_type_obj = super(RoleSubTypeSerializer, self).update(instance, validated_data)
            sub_type_obj.updated_by = user.id
            sub_type_obj.updated_date = datetime.utcnow()
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj

