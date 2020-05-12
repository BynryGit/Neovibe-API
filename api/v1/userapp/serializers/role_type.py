__author__ = "Arpita"

from rest_framework import serializers

from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.models.role_type import RoleType
from v1.utility.serializers.utility import UtilitySerializer


class RoleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleType
        fields = ('name', 'id_string')


class RoleTypeListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = RoleType
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')


class RoleTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = RoleType
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')
