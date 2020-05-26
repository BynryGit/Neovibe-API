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
        fields = ('id_string', 'module_name', 'module_desc', 'subscription_id', 'is_active', 'tenant', 'utility',)


class UtilityModuleSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('is_active',)

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_module_obj = super(UtilityModuleSerializer, self).update(instance, validated_data)
            utility_module_obj.updated_by = user.id
            utility_module_obj.updated_date = timezone.now()
            utility_module_obj.save()
            return utility_module_obj