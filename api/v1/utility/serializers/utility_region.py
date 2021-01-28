from rest_framework import serializers
from v1.utility.models.utility_region import UtilityRegion as UtilityRegionTbl


class UtilityRegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityRegionTbl
        fields = ('name', 'id_string','is_active','created_by','created_date')
