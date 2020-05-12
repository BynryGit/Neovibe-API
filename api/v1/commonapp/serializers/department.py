from rest_framework import serializers

from v1.commonapp.models.department import Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('status', 'id_string')


class DepartmentListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = Department
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'is_active')


class DepartmentViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = Department
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'is_active')
