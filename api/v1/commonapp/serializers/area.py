from rest_framework import serializers
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.area import Area
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer


# class GetAreaSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Area
#         fields = ('name', 'id_string')


class AreaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('name', 'id_string')


class AreaViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = Area
        fields = ('id_string', 'name', 'created_date', 'updated_date', 'tenant', 'utility')