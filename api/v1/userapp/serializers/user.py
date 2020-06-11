__author__ = "Arpita"
from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT
from master.models import User
from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.user_role import UserRole
from v1.userapp.models.user_status import UserStatus
from v1.userapp.models.user_sub_type import UserSubType
from v1.userapp.models.user_type import UserType
from v1.userapp.serializers.bank_detail import UserBankViewSerializer
from v1.userapp.serializers.role import GetRoleSerializer
from v1.userapp.views.common_functions import set_user_validated_data, set_user_role_validated_data


class UserSerializer(serializers.ModelSerializer):
    city_id = serializers.CharField(required=False, max_length=200)
    user_type_id = serializers.CharField(required=False, max_length=200)
    user_subtype_id = serializers.CharField(required=False, max_length=200)
    form_factor_id = serializers.CharField(required=False, max_length=200)
    department_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    bank_id = serializers.CharField(required=False, max_length=200)
    user_ID = serializers.CharField(required=False, max_length=200)
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
        if User.objects.filter(phone_mobile=validated_data['phone_mobile'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Mobile number already exists!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_obj = super(UserSerializer, self).create(validated_data)
                user_obj.set_password(validated_data['password'])
                user_obj.created_by = user.id
                user_obj.created_date = datetime.utcnow()
                user_obj.tenant = user.tenant
                user_obj.is_active = True
                user_obj.save()
                return user_obj

    def update(self, instance, validated_data, user):
        validated_data = set_user_validated_data(validated_data)
        if User.objects.exclude(id_string=instance.id_string).filter(phone_mobile=validated_data['phone_mobile'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Mobile number already exists!", status_code=status.HTTP_409_CONFLICT)
        else:
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

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = User
        fields = ('id_string', 'first_name', 'last_name', 'phone_mobile', 'email', 'created_date', 'tenant',
                  'department',  'status')


class UserViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    user_type = UserTypeSerializer(many=False, required=True, source='get_user_type')
    user_sub_type = UserSubTypeSerializer(many=False, required=True, source='get_user_sub_type')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    city = CitySerializer(many=False, required=True, source='get_city')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = User
        fields = ('id_string', 'first_name', 'middle_name', 'last_name', 'email', 'phone_mobile', 'phone_landline',
                  'created_date', 'tenant', 'user_type', 'user_sub_type', 'form_factor', 'city', 'department', 'status')


class UserRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    role_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_role_validated_data(validated_data)
        if UserRole.objects.filter(user_id=validated_data['user_id'], role_id=validated_data['role_id'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Role already exists for this user!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_role_obj = super(UserRoleSerializer, self).create(validated_data)
                user_role_obj.created_by = user.id
                user_role_obj.created_date = datetime.utcnow()
                user_role_obj.tenant = user.tenant
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

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    role = GetRoleSerializer(many=False, required=True, source='get_role')
    user = GetUserSerializer(many=False, required=True, source='get_user')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = RolePrivilege
        fields = ('id_string', 'tenant', 'role', 'user', 'created_date', 'is_active')
