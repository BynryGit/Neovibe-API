__author__ = "aki"

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_sub_module import UtilitySubModule as UtilitySubModuleTbl
from v1.utility.views.common_functions import set_utility_submodule_validated_data


class UtilitySubModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    utility_module = serializers.ReadOnlyField(source='get_utility_module')

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string', 'submodule_name', 'submodule_desc', 'utility_module', 'is_active', 'tenant', 'utility')


class UtilitySubModuleSerializer(serializers.ModelSerializer):
    submodule_id = serializers.UUIDField(required=True)

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string', 'tenant', 'utility', 'module_id', 'submodule_id', 'is_active', 'created_by',
                  'updated_by', 'created_date', 'updated_date')

    def create(self, validated_data, user):
        validated_data = set_utility_submodule_validated_data(validated_data)
        if UtilitySubModuleTbl.objects.filter(submodule_id=validated_data["submodule_id"]).exists():
            return False
        with transaction.atomic():
            utility_submodule_obj = super(UtilitySubModuleSerializer, self).create(validated_data)
            utility_submodule_obj.updated_by = user.id
            utility_submodule_obj.updated_date = timezone.now()
            utility_submodule_obj.save()
            return utility_submodule_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_submodule = super(UtilitySubModuleSerializer, self).update(instance, validated_data)
            utility_submodule.updated_by = user.id
            utility_submodule.updated_date = timezone.now()
            utility_submodule.save()
            return utility_submodule
