from rest_framework import serializers, status
from v1.utility.models.utility_product import UtilityProduct as UtilityProductTbl


class UtilityProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityProductTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')
