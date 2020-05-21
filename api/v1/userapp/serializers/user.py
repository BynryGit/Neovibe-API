__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.department import DepartmentSerializer
# from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.tenant.serializers.tenant import TenantSerializer, GetTenantSerializer
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.user_status import UserStatus
from v1.utility.serializers.utility import UtilitySerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'id_string')


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserListSerializer(serializers.ModelSerializer):
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    department = DepartmentSerializer(many=False, required=True, source='get_department')

    class Meta:
        model = UserDetail
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'department', 'first_name', 'last_name', 'user_ID', 'phone_mobile',
                  'status', 'email')


class UserViewSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user_type = UserTypeSerializer(many=False, required=True, source='get_user_type')
    user_sub_type = UserSubTypeSerializer(many=False, required=True, source='get_user_sub_type')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    city = CitySerializer(many=False, required=True, source='get_city')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    # bank = UserBankSerializer(many=False, required=True, source='get_bank')

    class Meta:
        model = UserDetail
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'user_type', 'user_sub_type', 'form_factor', 'city', 'department',
                  'status', 'user_ID','first_name', 'middle_name','last_name', 'email', 'user_image',
                  'phone_mobile', 'phone_landline', 'utilities', 'skills', 'areas', 'created_by', 'created_date')


class PrivilegeSerializer(serializers.ModelSerializer):
    # sub_module = SubModuleSerializer(many=True, required=True, source='get_all_submodules')

    class Meta:
        model = RolePrivilege
        fields = ('module_id', 'sub_module', 'privilege', 'id_string')


class RolePrivilegeSerializer(serializers.ModelSerializer):
    # sub_module = SubModuleSerializer(many=True, required=True, source='get_all_submodules')

    class Meta:
        model = RolePrivilege
        fields = ('module_id', 'sub_module', 'privilege', 'id_string')


class UserPrivilegeViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role_privileges = RolePrivilegeSerializer(many=True, required=True, source='get_role_privilege')

    class Meta:
        model = UserDetail
        fields = ('id_string', 'tenant', 'utility', 'role_privileges')