__author__ = "aki"

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_sub_module import UtilitySubModule as UtilitySubModuleTbl


class UtilitySubModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    utility_module = serializers.ReadOnlyField(source='get_utility_module')

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string', 'submodule_name', 'submodule_desc', 'utility_module', 'is_active', 'tenant', 'utility')


class UtilitySubModuleSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('is_active',)

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_submodule = super(UtilitySubModuleSerializer, self).update(instance, validated_data)
            utility_submodule.updated_by = user.id
            utility_submodule.updated_date = timezone.now()
            utility_submodule.save()
            return utility_submodule
