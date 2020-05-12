from rest_framework import serializers

from v1.userapp.models.role_type import RoleType


class RoleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleType
        fields = ('name', 'id_string')


class RoleTypeListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = RoleType
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'is_active')


class RoleTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = RoleType
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'is_active')
