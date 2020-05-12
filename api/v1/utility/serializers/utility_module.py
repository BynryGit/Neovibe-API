__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl


class UtilityModuleViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    utility = UtilityMasterViewSerializer(read_only=True)

    class Meta:
        model = UtilityModuleTbl
        fields = ('id_string', 'module_name', 'module_desc', 'tenant', 'utility',)