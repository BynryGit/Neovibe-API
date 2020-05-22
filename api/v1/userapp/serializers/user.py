__author__ = "Arpita"
from django.db import transaction
from datetime import datetime

from rest_framework import serializers

from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.user_role import UserRole
from v1.userapp.models.user_status import UserStatus
from v1.userapp.models.user_sub_type import UserSubType
from v1.userapp.models.user_type import UserType
from v1.userapp.serializers.bank_detail import UserBankViewSerializer
from v1.userapp.serializers.role import GetRoleSerializer
from v1.userapp.views.common_functions import set_user_validated_data, set_user_role_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class UserSerializer(serializers.ModelSerializer):
    city_id = serializers.CharField(required=False, max_length=200)
    user_type_id = serializers.CharField(required=False, max_length=200)
    user_subtype_id = serializers.CharField(required=False, max_length=200)
    form_factor_id = serializers.CharField(required=False, max_length=200)
    department_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    bank_id = serializers.CharField(required=False, max_length=200)
    user_ID = serializers.CharField(required=False, max_length=200)
    username = serializers.CharField(required=False, max_length=200)
    password = serializers.CharField(required=False, max_length=200)
    first_name = serializers.CharField(required=False, max_length=200)
    middle_name = serializers.CharField(required=False, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=False, max_length=200)
    phone_landline = serializers.CharField(required=False, max_length=200)
    utilities = serializers.JSONField(required=False)
    skills = serializers.JSONField(required=False)
    areas = serializers.JSONField(required=False)

    class Meta:
        model = UserDetail
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_validated_data(validated_data)
        with transaction.atomic():
            user_obj = super(UserSerializer, self).create(validated_data)
            user_obj.set_password(validated_data['password'])
            user_obj.created_by = user.id
            user_obj.created_date = datetime.utcnow()
            user_obj.tenant = user.tenant
            user_obj.utility = user.utility
            user_obj.is_active = True
            user_obj.save()
            return user_obj

    def update(self, instance, validated_data, user):
        validated_data = set_user_validated_data(validated_data)
        with transaction.atomic():
            user_obj = super(UserSerializer, self).update(instance, validated_data)
            if 'password' in validated_data:
                user_obj.set_password(validated_data['password'])
            user_obj.updated_by = user.id
            user_obj.updated_date = datetime.utcnow()
            user_obj.is_active = True
            user_obj.save()
            return user_obj


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = ('name', 'id_string')


class UserSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubType
        fields = ('name', 'id_string')


class UserListSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    department = DepartmentSerializer(many=False, required=True, source='get_department')

    class Meta:
        model = UserDetail
        fields = ('id_string', 'tenant', 'utility', 'department', 'first_name', 'last_name', 'user_ID', 'phone_mobile',
                  'status', 'email')


class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        fields = ('id_string', 'username', 'first_name', 'last_name')


class UserViewSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user_type = UserTypeSerializer(many=False, required=True, source='get_user_type')
    user_sub_type = UserSubTypeSerializer(many=False, required=True, source='get_user_sub_type')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    city = CitySerializer(many=False, required=True, source='get_city')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    bank = UserBankViewSerializer(many=False, required=True, source='get_user_bank')

    class Meta:
        model = UserDetail
        fields = ('id_string', 'tenant', 'utility', 'user_type', 'user_sub_type', 'form_factor', 'city', 'department',
                  'bank', 'status', 'user_ID','first_name', 'middle_name','last_name', 'email', 'user_image', 'phone_mobile',
                  'phone_landline', 'utilities', 'skills', 'areas', 'created_by', 'created_date')


class UserRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    role_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_role_validated_data(validated_data)
        with transaction.atomic():
            user_role_obj = super(UserRoleSerializer, self).create(validated_data)
            user_role_obj.created_by = user.id
            user_role_obj.created_date = datetime.utcnow()
            user_role_obj.tenant = user.tenant
            user_role_obj.utility = user.utility
            user_role_obj.is_active = True
            user_role_obj.save()
            return user_role_obj

    def update(self, instance, validated_data, user):
        validated_data = set_user_role_validated_data(validated_data)
        with transaction.atomic():
            user_role_obj = super(UserRoleSerializer, self).update(instance, validated_data)
            user_role_obj.updated_by = user.id
            user_role_obj.updated_date = datetime.utcnow()
            user_role_obj.save()
            return user_role_obj


class UserRoleViewSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    role = GetRoleSerializer(many=False, required=True, source='get_role')
    user = GetUserSerializer(many=False, required=True, source='get_user')

    class Meta:
        model = RolePrivilege
        fields = ('id_string', 'tenant', 'utility', 'role', 'user', 'created_date', 'is_active')
