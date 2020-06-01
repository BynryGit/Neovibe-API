__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_status import SupplierStatus as SupplierStatusTbl


class SupplierStatusViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = SupplierStatusTbl
        fields = ('id_string', 'name', 'tenant', 'utility')