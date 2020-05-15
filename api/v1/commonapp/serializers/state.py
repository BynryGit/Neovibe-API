__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.tenant.models.tenant_state import TenantState as TenantStateTbl


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantStateTbl
        fields = ('id_string', 'state')