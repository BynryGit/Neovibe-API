__author__ = "Gauri"

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.tenant.models.tenant_sub_module import TenantSubModule as TenantSubModuleTbl


class TenantSubModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    tenant_module = serializers.ReadOnlyField(source='get_tenant_module')

    class Meta:
        model = TenantSubModuleTbl
        fields = ('sub_module_id', 'sub_module_name', 'submodule_desc', 'subscription_id', 'module_id')


class TenantSubModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantSubModuleTbl
        fields = ('sub_module_id', 'sub_module_name', 'submodule_desc', 'subscription_id', 'module_id')

    def create(self, validated_data, user):
        with transaction.atomic():
            tenant_module = super(TenantSubModuleSerializer, self).create(validated_data)
            tenant_module.created_by = user
            tenant_module.save()
            return tenant_module

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            tenant_module = super(TenantSubModuleSerializer, self).update(instance, validated_data)
            tenant_module.updated_by = user
            tenant_module.updated_date = timezone.now()
            tenant_module.save()
            return tenant_module