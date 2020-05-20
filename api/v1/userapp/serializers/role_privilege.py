__author__ = "Arpita"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.views.common_functions import set_role_privilege_validated_data


class RolePrivilegeSerializer(serializers.ModelSerializer):
    role_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    privilege_id = serializers.CharField(required=False, max_length=200)

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


class RolePrivilegeViewSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')
    role_sub_type = RoleSubTypeSerializer(many=False, required=True, source='get_role_sub_type')

    class Meta:
        model = Role
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'department', 'form_factor', 'role_type', 'role_sub_type',
                  'role_ID', 'role', 'created_date', 'is_active')