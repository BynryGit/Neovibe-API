__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.tender.models.tender_status import TenderStatus as TenderStatusTbl


class TenderStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenderStatusTbl
        fields = ('id_string', 'status')


class TenderStatusViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = TenderStatusTbl
        fields = ('id_string', 'status', 'tenant', 'utility')
