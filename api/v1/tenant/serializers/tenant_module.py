__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl


class TenantModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'module_name', 'module_desc', 'tenant')


class TenantModuleSerializer(serializers.ModelSerializer):
    utility_id_string = serializers.UUIDField(required=True, source='utility.id_string')

    class Meta:
        model = UtilityModuleTbl
        fields = ('tenant_id_string', 'subscription_id', 'module_name', 'module_desc')

    def create(self, validated_data, user):
        with transaction.atomic():
            tenant_module = super(TenantModuleSerializer, self).create(validated_data)
            tenant_module.created_by = user
            tenant_module.save()
            return tenant_module

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            tenant_module = super(TenantModuleSerializer, self).update(instance, validated_data)
            tenant_module.updated_by = user
            tenant_module.updated_date = timezone.now()
            tenant_module.save()
            return tenant_module