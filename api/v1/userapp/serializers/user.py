__author__ = "Arpita"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status
import random

from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from master.models import User
from v1.commonapp.serializers.city import CitySerializer
from v1.commonapp.serializers.department import DepartmentSerializer
from v1.commonapp.serializers.form_factor import FormFactorSerializer
from v1.supplier.serializers.supplier import SupplierViewSerializer
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.role import get_role_by_id
from v1.userapp.models.user_role import get_role_count_by_user, get_user_role_by_user_id
from v1.userapp.models.user_status import UserStatus
from v1.userapp.models.user_sub_type import UserSubType
from v1.userapp.models.user_type import UserType
from v1.userapp.views.common_functions import set_user_validated_data, generate_user_id

from v1.userapp.serializers.role import GetRoleSerializer
from v1.userapp.serializers.user_role import UserRoleViewSerializer
from v1.userapp.views.common_functions import set_user_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.userapp.models.login_trail import LoginTrail
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.password_validation import validate_password

l1 = LoginTrail


class UserSerializer(serializers.ModelSerializer):
    city_id = serializers.CharField(required=False, max_length=200)
    user_type_id = serializers.CharField(required=False, max_length=200)
    user_subtype_id = serializers.CharField(required=False, max_length=200)
    form_factor_id = serializers.CharField(required=False, max_length=200)
    department_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    supplier_id = serializers.CharField(required=False, max_length=200)
    email = serializers.CharField(required=False, max_length=200)
    password = serializers.CharField(required=False, max_length=200)
    first_name = serializers.CharField(required=False, max_length=200)
    middle_name = serializers.CharField(required=False, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=False, max_length=200)
    phone_landline = serializers.CharField(required=False, max_length=200)

    # last_login = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_validated_data(validated_data)
        if User.objects.filter(email=validated_data['email'], is_active=True).exists():
            raise CustomAPIException("User already exists ! ", status_code=status.HTTP_409_CONFLICT)

        with transaction.atomic():
            user_obj = super(UserSerializer, self).create(validated_data)
            user_obj.set_password(validated_data['password'])
            user_obj.created_by = user.id
            user_obj.created_date = datetime.utcnow()
            user_obj.joined_date = datetime.utcnow()
            user_obj.last_login = datetime.utcnow()
            user_obj.tenant = user.tenant
            user_obj.status_id = 2
            user_obj.is_active = True
            # user_obj.save()
#             user_obj.user_id = generate_user_id(user_obj)
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
        fields = ('id_string', 'email', 'user_id', 'first_name', 'last_name', 'phone_mobile')


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
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    role = serializers.SerializerMethodField('get_role')
    user_type = serializers.CharField(required=False, max_length=200, source='get_user_type')
    user_department = serializers.CharField(required=False, max_length=200, source='get_department')

    class Meta:
        model = User
        fields = (
            'id_string', 'user_id', 'first_name', 'last_name', 'phone_mobile', 'email', 'created_date', 'updated_date',
            'role', 'tenant', 'department', 'status', 'user_type', 'user_department')


class UserViewSerializer(serializers.ModelSerializer):
    # def get_role(self, obj):
    #     role_list = []
    #     user_roles = get_user_role_by_user_id(obj.id)
    #     for user_role in user_roles:
    #         role = get_role_by_id(user_role.role_id)
    #         serializer = GetRoleSerializer(instance=role)
    #         role_list.append(serializer.data)
    #     return role_list

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    user_type = UserTypeSerializer(many=False, required=True, source='get_role_type')
    user_sub_type = UserSubTypeSerializer(many=False, required=True, source='get_role_sub_type')
    form_factor = FormFactorSerializer(many=False, required=True, source='get_form_factor')
    status = UserStatusSerializer(many=False, required=True, source='get_user_status')
    city = CitySerializer(many=False, required=True, source='get_city')
    department = DepartmentSerializer(many=False, required=True, source='get_department')
    supplier = SupplierViewSerializer(many=False, required=True, source='get_supplier')
    # roles = serializers.SerializerMethodField('get_role')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = User
        fields = ('id_string', 'first_name', 'middle_name', 'last_name', 'email', 'phone_mobile', 'phone_landline',
                  'user_id', 'created_date', 'updated_date', 'tenant', 'user_type', 'user_sub_type', 'form_factor',
                  'city',
                  'department', 'status', 'supplier')


class UserShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id_string', 'first_name', 'last_name', 'email')


# class ChangePasswordSerializer(serializers.ModelSerializer):
#
#
#     class Meta:
#         model = User
#         fields = ('old_password', 'new_password')
#
#     # def validate(self, attrs):
#     #     if attrs['password'] != attrs['password2']:
#     #         raise serializers.ValidationError({"password": "Password fields didn't match."})
#     #
#     #     return attrs
#
#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value
#
#     def update(self, instance, validated_data):
#
#         instance.set_password(validated_data['new_password'])
#         instance.save()
#         print("INSTANCE",instance)
#
#         return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    old_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('password', 'old_password')


    def update(self, instance, validated_data, user):
        with transaction.atomic():
            user_obj = super(ChangePasswordSerializer, self).update(instance, validated_data)
            user_obj.updated_by = user.id
            user_obj.password = instance.set_password(validated_data['password'])
            print("YHCYCHCHC",instance.set_password(validated_data['password']))
            user_obj.updated_date = datetime.utcnow()
            user_obj.save()
            return user_obj




class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
