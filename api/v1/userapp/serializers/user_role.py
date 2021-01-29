__author__ = "Arpita"
from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.userapp.models.user_role import UserRole
from v1.userapp.serializers.role import RoleViewSerializer
from v1.userapp.views.common_functions import set_user_role_validated_data


class UserRoleSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    user_id = serializers.CharField(required=False, max_length=200)
    role_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

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
                user_role_obj.updated_by = user.id
                user_role_obj.created_date = datetime.utcnow()
                user_role_obj.update_date = datetime.utcnow()
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

    role = RoleViewSerializer(many=False, required=True, source='get_role')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = UserRole
        fields = ('id_string', 'created_date', 'updated_date', 'role')
