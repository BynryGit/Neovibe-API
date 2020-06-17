__author__ = "Arpita"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer, SubModuleViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_privilege import UserPrivilege
from v1.userapp.serializers.privilege import GetPrivilegeSerializer
from v1.userapp.serializers.user import GetUserSerializer
from v1.userapp.views.common_functions import set_user_privilege_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class UserPrivilegeSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    privilege_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserPrivilege
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_user_privilege_validated_data(validated_data)
        if UserPrivilege.objects.filter(user_id=validated_data['user_id'], module_id=validated_data['module_id'],
                                        sub_module_id=validated_data['sub_module_id'],
                                        privilege_id=validated_data['privilege_id'], tenant=user.tenant,
                                        is_active=True).exists():
            raise CustomAPIException("Privilege already exists for specified user!",
                                     status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_privilege_obj = super(UserPrivilegeSerializer, self).create(validated_data)
                user_privilege_obj.created_by = user.id
                user_privilege_obj.updated_by = user.id
                user_privilege_obj.created_date = datetime.utcnow()
                user_privilege_obj.updated_date = datetime.utcnow()
                user_privilege_obj.tenant = user.tenant
                user_privilege_obj.is_active = True
                user_privilege_obj.save()
                return user_privilege_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            user_privilege_obj = super(UserPrivilegeSerializer, self).update(instance, validated_data)
            user_privilege_obj.updated_by = user.id
            user_privilege_obj.updated_date = datetime.utcnow()
            user_privilege_obj.save()
            return user_privilege_obj


class UserPrivilegeViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user = GetUserSerializer(many=False, required=True, source='get_user')
    # module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    # privilege = GetPrivilegeSerializer(many=False, required=True, source='get_privilege')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = UserPrivilege
        fields = ('id_string', 'created_date', 'updated_date', 'tenant', 'utility', 'user', 'sub_module')