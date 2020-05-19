__author__ = "Arpita"
from django.db import transaction
from rest_framework import serializers
from datetime import datetime
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.models.role_status import RoleStatus
from v1.userapp.models.role import UserRole
from v1.userapp.serializers.role_sub_type import RoleSubTypeSerializer
from v1.userapp.serializers.role_type import RoleTypeSerializer
from v1.userapp.views.common_functions import set_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class RoleSerializer(serializers.ModelSerializer):
    type_id = serializers.CharField(required=False, max_length=200)
    sub_type_id = serializers.CharField(required=False, max_length=200)
    form_factor_id = serializers.CharField(required=False, max_length=200)
    department_id = serializers.CharField(required=False, max_length=200)
    role_ID = serializers.CharField(required=False, max_length=200)
    role = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data =  set_validated_data(validated_data)
        with transaction.atomic():
            role_obj = super(RoleSerializer, self).create(validated_data)
            role_obj.created_by = user.id
            role_obj.created_date = datetime.utcnow()
            role_obj.tenant = user.tenant
            role_obj.utility = user.utility
            role_obj.is_active = True
            role_obj.save()
            return role_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            role_obj = super(RoleSerializer, self).update(instance, validated_data)
            role_obj.updated_by = user.id
            role_obj.updated_date = datetime.utcnow()
            role_obj.save()
            return role_obj


class RoleStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleStatus
        fields = ('status', 'id_string')


class RoleListSerializer(serializers.ModelSerializer):
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')
    role_sub_type = RoleSubTypeSerializer(many=False, required=True, source='get_role_sub_type')

    class Meta:
        model = UserRole
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'role', 'role_ID', 'role_type', 'role_sub_type', 'form_factor',
                  'department', 'created_date')


class RoleViewSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')
    role_sub_type = RoleSubTypeSerializer(many=False, required=True, source='get_role_sub_type')

    class Meta:
        model = UserRole
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'department', 'form_factor', 'role_type', 'role_sub_type',
                  'role_ID', 'role', 'created_date', 'is_active')
