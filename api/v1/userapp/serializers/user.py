__author__ = "Arpita"
from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT
from master.models import User
from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_role import get_role_count_by_user
from v1.userapp.models.user_status import UserStatus
from v1.userapp.models.user_sub_type import UserSubType
from v1.userapp.models.user_type import UserType
from v1.userapp.views.common_functions import set_user_validated_data


class UserSerializer(serializers.ModelSerializer):
    city_id = serializers.CharField(required=False, max_length=200)
    user_type_id = serializers.CharField(required=False, max_length=200)
    user_subtype_id = serializers.CharField(required=False, max_length=200)
    form_factor_id = serializers.CharField(required=False, max_length=200)
    department_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    email = serializers.CharField(required=False, max_length=200)
    password = serializers.CharField(required=False, max_length=200)
    first_name = serializers.CharField(required=False, max_length=200)
    middle_name = serializers.CharField(required=False, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=False, max_length=200)
    phone_landline = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_validated_data(validated_data)
        with transaction.atomic():
            user_obj = super(UserSerializer, self).create(validated_data)
            user_obj.set_password(validated_data['password'])
            user_obj.created_by = user.id
            user_obj.updated_by = user.id
            user_obj.created_date = datetime.utcnow()
            user_obj.updated_date = datetime.utcnow()
            user_obj.tenant = user.tenant
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


class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id_string')


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('id_string', 'status')


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = ('name', 'id_string')


class UserSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubType
        fields = ('name', 'id_string')


class UserListSerializer(serializers.ModelSerializer):

    def get_role(self, obj):
        role = get_role_count_by_user(obj.id)
        return role

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    role = serializers.SerializerMethodField('get_role')

    class Meta:
        model = User
        fields = ('id_string', 'first_name', 'last_name', 'phone_mobile', 'email', 'created_date', 'updated_date',
                  'role', 'tenant', 'department',  'status')


class UserViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    user_type = UserTypeSerializer(many=False, required=True, source='get_user_type')
    user_sub_type = UserSubTypeSerializer(many=False, required=True, source='get_user_sub_type')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    city = CitySerializer(many=False, required=True, source='get_city')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = User
        fields = ('id_string', 'first_name', 'middle_name', 'last_name', 'email', 'phone_mobile', 'phone_landline',
                  'created_date', 'updated_date', 'tenant', 'user_type', 'user_sub_type', 'form_factor', 'city', 'department', 'status')
