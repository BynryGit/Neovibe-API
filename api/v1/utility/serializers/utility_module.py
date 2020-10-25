__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl
from v1.utility.views.common_functions import set_utility_module_validated_data


class UtilityModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'module_name', 'module_desc', 'subscription_id', 'is_active', 'tenant', 'utility',)


class UtilityModuleSerializer(serializers.ModelSerializer):
    module_id = serializers.UUIDField(required=True)

    class Meta:
        model = UtilityModuleTbl
        # fields = ('id_string', 'module_name','is_active',)
        fields = ('id_string', 'tenant', 'utility', 'subscription_id', 'module_id', 'is_active', 'created_by',
                  'updated_by', 'created_date', 'updated_date')

    def create(self, validated_data, user):
        validated_data = set_utility_module_validated_data(validated_data)
        if UtilityModuleTbl.objects.filter(module_id=validated_data["module_id"]).exists():
            return False
        with transaction.atomic():
            utility_module_obj = super(UtilityModuleSerializer, self).create(validated_data)
            utility_module_obj.updated_by = user.id
            utility_module_obj.updated_date = timezone.now()
            utility_module_obj.save()
            return utility_module_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_module_obj = super(UtilityModuleSerializer, self).update(instance, validated_data)
            utility_module_obj.updated_by = user.id
            utility_module_obj.updated_date = timezone.now()
            utility_module_obj.save()
            return utility_module_obj
