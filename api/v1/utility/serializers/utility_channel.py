from rest_framework import serializers
from v1.utility.models.utility_channel import UtilityChannel as UtilityChannelTbl


class UtilityChannelListSerializer(serializers.ModelSerializer):
    utility = serializers.ReadOnlyField(source='utility.name')

    class Meta:
        model = UtilityChannelTbl
        fields = ('utility', 'name', 'id_string', 'is_active', 'created_by', 'created_date')
