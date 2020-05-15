__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl


class UtilityModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'module_name', 'module_desc', 'tenant', 'utility',)


class UtilityModuleSerializer(serializers.ModelSerializer):
    utility_id_string = serializers.UUIDField(required=True, source='utility.id_string')

    class Meta:
        model = UtilityModuleTbl
        fields = ('utility_id_string', 'subscription_id', 'module_name', 'module_desc')

    def create(self, validated_data, user):
        with transaction.atomic():
            utility_module = super(UtilityModuleSerializer, self).create(validated_data)
            utility_module.created_by = user
            utility_module.save()
            return utility_module

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_module = super(UtilityModuleSerializer, self).update(instance, validated_data)
            utility_module.updated_by = user
            utility_module.updated_date = timezone.now()
            utility_module.save()
            return utility_module