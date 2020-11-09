from rest_framework import serializers
from v1.commonapp.serializers.region import RegionSerializer
from v1.utility.models.utility_region import UtilityRegion

class UtilityRegionListSerializer(serializers.ModelSerializer):
    region = RegionSerializer(many=False, source='get_region')

    class Meta:
        model = UtilityRegion
        fields = ('id_string', 'label', 'region')
