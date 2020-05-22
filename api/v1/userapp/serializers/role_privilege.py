__author__ = "Arpita"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.serializers.privilege import GetPrivilegeSerializer
from v1.userapp.serializers.role import GetRoleSerializer
from v1.userapp.views.common_functions import set_role_privilege_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class RolePrivilegeSerializer(serializers.ModelSerializer):
    role_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    privilege_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = RolePrivilege
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_role_privilege_validated_data(validated_data)
        with transaction.atomic():
            role_privilege_obj = super(RolePrivilegeSerializer, self).create(validated_data)
            role_privilege_obj.created_by = user.id
            role_privilege_obj.created_date = datetime.utcnow()
            role_privilege_obj.tenant = user.tenant
            role_privilege_obj.utility = user.utility
            role_privilege_obj.is_active = True
            role_privilege_obj.save()
            return role_privilege_obj

    def update(self, instance, validated_data, user):
        validated_data = set_role_privilege_validated_data(validated_data)
        with transaction.atomic():
            role_obj = super(RolePrivilegeSerializer, self).update(instance, validated_data)
            role_obj.updated_by = user.id
            role_obj.updated_date = datetime.utcnow()
            role_obj.save()
            return role_obj


class RolePrivilegeViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role = GetRoleSerializer(many=False, required=True, source='get_role')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    privilege = GetPrivilegeSerializer(many=False, required=True, source='get_privilege')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = RolePrivilege
        fields = ('id_string', 'tenant', 'utility', 'role', 'module', 'sub_module', 'privilege',
                  'created_date', 'is_active')