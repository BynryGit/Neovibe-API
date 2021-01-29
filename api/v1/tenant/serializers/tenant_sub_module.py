__author__ = "aki"

from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone
from api.messages import SUBMODULE_ALREADY_EXIST
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_sub_module import TenantSubModule as TenantSubModuleTbl
from v1.tenant.views.common_functions import set_tenant_sub_module_validated_data


class TenantSubModuleViewSerializer(serializers.ModelSerializer):
    module_id = ModuleSerializer(many=False, required=False, source='get_module')
    sub_module_id = ModuleSerializer(many=False, required=False, source='get_sub_module')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = TenantSubModuleTbl
        fields = ('id_string', 'created_date', 'updated_date', 'module_id', 'sub_module_id')


class TenantSubModuleSerializer(serializers.ModelSerializer):
    sub_module_id = serializers.UUIDField(required=True)

    class Meta:
        model = TenantSubModuleTbl
        fields = ('__all__')

    def create(self, validated_data, tenant_obj, user):
        validated_data = set_tenant_sub_module_validated_data(validated_data)
        if TenantSubModuleTbl.objects.filter(tenant=tenant_obj, module_id=validated_data["module_id"],
                                             sub_module_id=validated_data["sub_module_id"]).exists():
            raise CustomAPIException(SUBMODULE_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_sub_module_obj = super(TenantSubModuleSerializer, self).create(validated_data)
            tenant_sub_module_obj.tenant = tenant_obj
            tenant_sub_module_obj.created_by = user.id
            tenant_sub_module_obj.save()
            return tenant_sub_module_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tenant_sub_module_validated_data(validated_data)
        with transaction.atomic():
            tenant_sub_module_obj = super(TenantSubModuleSerializer, self).update(instance, validated_data)
            tenant_sub_module_obj.updated_date = timezone.now()
            tenant_sub_module_obj.save()
            return tenant_sub_module_obj
