from rest_framework import serializers

from v1.commonapp.models.sub_module import SubModule
from v1.commonapp.serializers.module import ModuleSerializer


class SubModuleListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'module', 'name',
                  'is_active')


class SubModuleViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'module', 'name',
                  'is_active')
