__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.tender.models.tender_type import TenderType as TenderTypeTbl


class TenderTypeShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenderTypeTbl
        fields = ('id_string', 'type')


class TenderTypeViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()

    class Meta:
        model = TenderTypeTbl
        fields = ('id_string', 'type', 'tenant', 'utility')