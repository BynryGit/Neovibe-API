__author__ = "aki"

from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone
from api.messages import MODULE_ALREADY_EXIST
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_module import TenantModule as TenantModuleTbl
from v1.tenant.views.common_functions import set_tenant_module_validated_data


class TenantModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    module_id = ModuleSerializer(many=False, required=False, source='get_module')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantModuleTbl
        fields = ('id_string', 'created_date', 'updated_date', 'tenant', 'module_id')


class TenantModuleSerializer(serializers.ModelSerializer):
    module_id = serializers.UUIDField(required=True)

    class Meta:
       model = TenantModuleTbl
       fields = ('__all__')

    def create(self, validated_data, tenant_obj, user):
        validated_data = set_tenant_module_validated_data(validated_data)
        if TenantModuleTbl.objects.filter(tenant=tenant_obj, module_id=validated_data["module_id"]).exists():
            raise CustomAPIException(MODULE_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_module_obj = super(TenantModuleSerializer, self).create(validated_data)
            tenant_module_obj.tenant = tenant_obj
            tenant_module_obj.created_by = user.id
            tenant_module_obj.save()
            return tenant_module_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tenant_module_validated_data(validated_data)
        with transaction.atomic():
            tenant_module_obj = super(TenantModuleSerializer, self).update(instance, validated_data)
            tenant_module_obj.updated_date = timezone.now()
            tenant_module_obj.save()
            return tenant_module_obj
