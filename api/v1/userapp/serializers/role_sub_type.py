__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.serializers.role_type import RoleTypeSerializer
from v1.commonapp.views.role_sub_type import RoleSubType


class RoleSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleSubType
        fields = ('name', 'id_string')


class RoleSubTypeListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')

    class Meta:
        model = RoleSubType
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'role_type', 'name',
                  'is_active')


class RoleSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')

    class Meta:
        model = RoleSubType
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'role_type', 'name',
                  'is_active')
