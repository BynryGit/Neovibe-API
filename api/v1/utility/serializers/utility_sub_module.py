__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_sub_module import UtilitySubModule as UtilitySubModuleTbl


class UtilitySubModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)
    utility_module = serializers.ReadOnlyField(source='get_utility_module')

    class Meta:
        model = UtilitySubModuleTbl
        fields = ('id_string', 'submodule_name', 'submodule_desc', 'utility_module', 'tenant', 'utility',)