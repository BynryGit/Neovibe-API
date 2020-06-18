__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.department import Department
from v1.tenant.serializers.tenant import TenantMasterViewSerializer
from v1.utility.serializers.utility import UtilitySerializer


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id_string', 'name')


class DepartmentListSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = Department
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')


class DepartmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = Department
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')
