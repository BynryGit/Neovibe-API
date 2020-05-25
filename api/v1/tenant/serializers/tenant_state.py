__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_state import TenantState as TenantStateTbl


class TenantStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantStateTbl
        fields = ('id_string', 'name')