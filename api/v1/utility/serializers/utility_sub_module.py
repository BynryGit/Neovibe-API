__author__ = "aki"

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.module import ModuleShortViewSerializer
from v1.commonapp.serializers.sub_module import SubModuleShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_sub_module import UtilitySubModule as UtilitySubModuleTbl
from v1.utility.views.common_functions import set_utility_submodule_validated_data
from v1.commonapp.models.sub_module import SubModule as SubModuleTbl


class UtilitySubModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    module_id = ModuleShortViewSerializer(many=False, source='get_module')
    submodule_id = SubModuleShortViewSerializer(many=False, source='get_submodule')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string', 'label', 'created_date', 'updated_date', 'is_active', 'module_id', 'submodule_id',
                  'tenant', 'utility')


class UtilitySubModuleSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(required=False, source='tenant.id_string')
    utility = serializers.UUIDField(required=False, source='utility.id_string')
    module_id = serializers.UUIDField(required=True)
    submodule_id = serializers.UUIDField(required=True)

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string', 'tenant', 'utility', 'module_id', 'submodule_id', 'is_active', 'created_by',
                  'updated_by', 'created_date', 'updated_date')

    def create(self, validated_data, user):
        validated_data = set_utility_submodule_validated_data(validated_data)
        if UtilitySubModuleTbl.objects.filter(tenant=validated_data["tenant"], utility=validated_data["utility"],
                                              module_id=validated_data["module_id"],
                                              submodule_id=validated_data["submodule_id"]).exists():
            return False
        with transaction.atomic():
            if 'tenant' in validated_data:
                tenant = validated_data.pop('tenant')
            if 'utility' in validated_data:
                utility = validated_data.pop('utility')
            utility_submodule_obj = super(UtilitySubModuleSerializer, self).create(validated_data)
            utility_submodule_obj.updated_by = user.id
            utility_submodule_obj.updated_date = timezone.now()
            utility_submodule_obj.tenant_id = tenant
            utility_submodule_obj.utility_id = utility
            utility_submodule_obj.save()
            return utility_submodule_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_submodule = super(UtilitySubModuleSerializer, self).update(instance, validated_data)
            utility_submodule.updated_by = user.id
            utility_submodule.updated_date = timezone.now()
            utility_submodule.save()
            return utility_submodule
    
    def destroy(self, instance, validated_data, user):
        with transaction.atomic():
            utility_submodule_obj = super(UtilitySubModuleSerializer, self).destroy(instance, validated_data)
            utility_submodule_obj.updated_by = user.id
            utility_submodule_obj.updated_date = timezone.now()
            utility_submodule_obj.save()
            return utility_submodule_obj
   


class UtilitySubModuleListSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string','label')



