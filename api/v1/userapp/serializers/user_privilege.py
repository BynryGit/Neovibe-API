__author__ = "Arpita"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.user_privilege import UserPrivilege
from v1.userapp.serializers.privilege import GetPrivilegeSerializer
from v1.userapp.serializers.user import GetUserSerializer
from v1.utility.serializers.utility import UtilitySerializer


class UserPrivilegeSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    privilege_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = UserPrivilege
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            user_privilege_obj = super(UserPrivilegeSerializer, self).create(validated_data)
            user_privilege_obj.created_by = user.id
            user_privilege_obj.created_date = datetime.utcnow()
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

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user = GetUserSerializer(many=False, required=True, source='get_user')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    privilege = GetPrivilegeSerializer(many=False, required=True, source='get_privilege')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserPrivilege
        fields = ('id_string', 'tenant', 'utility', 'user', 'module', 'sub_module', 'privilege',
                  'created_date', 'is_active')