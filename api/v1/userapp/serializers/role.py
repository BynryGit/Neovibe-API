__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.models.role_status import RoleStatus
from v1.userapp.models.role import UserRole
from v1.userapp.serializers.role_sub_type import RoleSubTypeSerializer
from v1.userapp.serializers.role_type import RoleTypeSerializer
from v1.utility.serializers.utility import UtilitySerializer


class RoleStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleStatus
        fields = ('status', 'id_string')


class RoleListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    status = RoleStatusSerializer(many=False, required=True, source='get_role_status')
    role_type = serializers.ReadOnlyField(source='get_role_type')
    role_sub_type = serializers.ReadOnlyField(source='get_role_sub_type')
    form_factor = serializers.ReadOnlyField(source='get_form_factor')
    department = serializers.ReadOnlyField(source='get_department')

    class Meta:
        model = UserRole
        fields = ('id_string', 'tenant', 'utility', 'name', 'role_type', 'role_sub_type', 'status', 'form_factor',
                  'department', 'created_on')


class RoleViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')
    role_sub_type = RoleSubTypeSerializer(many=False, required=True, source='get_role_sub_type')

    class Meta:
        model = UserRole
        fields = ('id_string', 'tenant', 'utility', 'department', 'form_factor', 'role_type', 'role_sub_type',
                  'role_ID', 'role', 'created_on', 'privilege_list', 'is_active')
