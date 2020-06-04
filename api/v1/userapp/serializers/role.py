__author__ = "Arpita"
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator

from datetime import datetime

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.role import Role
from v1.userapp.serializers.role_sub_type import RoleSubTypeSerializer
from v1.userapp.serializers.role_type import RoleTypeSerializer
from v1.userapp.views.common_functions import set_role_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class RoleSerializer(serializers.ModelSerializer):
    type_id = serializers.CharField(required=False, max_length=200)
    sub_type_id = serializers.CharField(required=False, max_length=200)
    form_factor_id = serializers.CharField(required=False, max_length=200)
    department_id = serializers.CharField(required=False, max_length=200)
    role_ID = serializers.CharField(required=False, max_length=200)
    role = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_role_validated_data(validated_data)
        if Role.objects.filter(role=validated_data['role'], type_id=validated_data['type_id'], sub_type_id=validated_data['sub_type_id'], form_factor_id=validated_data['form_factor_id'], department_id=validated_data['department_id'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Role already exists!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                role_obj = super(RoleSerializer, self).create(validated_data)
                role_obj.created_by = user.id
                role_obj.created_date = datetime.utcnow()
                role_obj.tenant = user.tenant
                role_obj.is_active = True
                role_obj.save()
                role_obj.role_ID = str(role_obj.role) + str(role_obj.tenant) + str(role_obj.utility)
                role_obj.save()
                return role_obj

    def update(self, instance, validated_data, user):
        validated_data = set_role_validated_data(validated_data)
        if Role.objects.exclude(id_string=instance.id_string).filter(role=validated_data['role'], type_id=validated_data['type_id'], sub_type_id=validated_data['sub_type_id'], form_factor_id=validated_data['form_factor_id'], department_id=validated_data['department_id'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Role already exists!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                role_obj = super(RoleSerializer, self).update(instance, validated_data)
                role_obj.updated_by = user.id
                role_obj.updated_date = datetime.utcnow()
                role_obj.is_active = True
                role_obj.save()
                return role_obj


class RoleListSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')
    role_sub_type = RoleSubTypeSerializer(many=False, required=True, source='get_role_sub_type')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = Role
        fields = ('id_string', 'tenant', 'utility', 'form_factor', 'department', 'role_type', 'role_sub_type', 'role',
                  'role_ID',  'created_date')


class RoleViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    role_type = RoleTypeSerializer(many=False, required=True, source='get_role_type')
    role_sub_type = RoleSubTypeSerializer(many=False, required=True, source='get_role_sub_type')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = Role
        fields = ('id_string', 'tenant', 'utility', 'department', 'form_factor', 'role_type', 'role_sub_type',
                  'role_ID', 'role', 'created_date', 'is_active')


class GetRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('id_string', 'role_ID', 'role')
