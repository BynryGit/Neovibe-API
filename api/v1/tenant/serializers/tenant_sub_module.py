__author__ = "Gauri"

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.tenant.models.tenant_sub_module import TenantSubModule as TenantSubModuleTbl
from v1.tenant.views.common_functions import set_validated_data, set_validated_data_submodule

class TenantSubmoduleListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantSubModuleTbl
        fields = ('id_string', 'sub_module_name', 'submodule_desc', 'subscription_id', 'module_id')



class TenantSubModuleViewSerializer(serializers.ModelSerializer):
    # tenant = TenantMasterViewSerializer(read_only=True)
    # tenant_module = serializers.ReadOnlyField(source='get_tenant_module')

    class Meta:
        model = TenantSubModuleTbl
        fields = ('id_string', 'sub_module_name', 'submodule_desc', 'subscription_id', 'module_id')


class TenantSubModuleSerializer(serializers.ModelSerializer):
     id_string = serializers.CharField(required=False, max_length=200)
     sub_module_name = serializers.CharField(required=False, max_length=200)
     submodule_desc = serializers.CharField(required=False, max_length=200)
     subscription_id = serializers.CharField(required=False, max_length=200)
     module_id = serializers.CharField(required=False, max_length=200)

     class Meta:
        model = TenantSubModuleTbl
        fields = ('__all__')

     def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            print("Check for this")
            tenant_sub_module = super(TenantSubModuleSerializer, self).create(validated_data)

            # tenant_module.created_by = user
            tenant_sub_module.save()
            return tenant_sub_module

     def update(self, instance, validated_data,user):
        validated_data = set_validated_data_submodule(validated_data)
        with transaction.atomic():
            tenant_sub_module = super(TenantSubModuleSerializer, self).update(instance, validated_data)
            # tenant_sub_module.updated_by = user
            tenant_sub_module.updated_date = timezone.now()
            tenant_sub_module.save()
            return tenant_sub_module