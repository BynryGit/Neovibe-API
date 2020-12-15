from rest_framework import serializers
from v1.commonapp.models.lifecycle import LifeCycle
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer


class LifeCycleListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_tenant')

    class Meta:
        model = LifeCycle
        fields = ('__all__')