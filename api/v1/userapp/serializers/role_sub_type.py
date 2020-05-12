__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.serializers.role_type import RoleTypeSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.models.role_sub_type import RoleSubType
from v1.utility.serializers.utility import UtilitySerializer


class RoleSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleSubType
        fields = ('name', 'id_string')


class RoleSubTypeListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')

    class Meta:
        model = RoleSubType
        fields = ('id_string', 'tenant', 'utility', 'role_type', 'name', 'is_active')


class RoleSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')

    class Meta:
        model = RoleSubType
        fields = ('id_string', 'tenant', 'utility', 'role_type', 'name', 'is_active')
