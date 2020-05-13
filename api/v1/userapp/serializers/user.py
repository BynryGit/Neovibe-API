__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.user_status import UserStatus
from v1.utility.serializers.utility import UtilitySerializer


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    department = DepartmentSerializer(many=False, required=True, source='get_department')

    class Meta:
        model = UserDetail
        fields = ('id_string', 'tenant', 'utility', 'name', 'user_ID', 'contact', 'status', 'email', 'department', 'role')


class UserViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    city = CitySerializer(many=False, required=True, source='get_city')
    department = DepartmentSerializer(many=False, required=True, source='get_department')

    class Meta:
        model = UserDetail
        fields = ('id_string', 'tenant', 'utility', 'user_ID','first_name', 'middle_name','last_name', 'email', 'type',
                  'sub_type', 'role', 'form_factor', 'city', 'department', 'street', 'status', 'roles', 'privileges',
                  'skills', 'areas')
