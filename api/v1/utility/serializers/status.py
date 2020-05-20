__author__ = "aki"

from rest_framework import serializers
from v1.utility.models.utility_status import UtilityStatus as UtilityStatusTbl


class UtilityStatusViewSerializer(serializers.ModelSerializer):
    utility_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = UtilityStatusTbl
        fields = ('id_string', 'utility_name', 'status', 'is_active')