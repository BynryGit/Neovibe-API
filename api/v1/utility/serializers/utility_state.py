from rest_framework import serializers
from v1.commonapp.serializers.state import StateSerializer
from v1.utility.models.utility_state import UtilityState

class UtilityStateListSerializer(serializers.ModelSerializer):
    state = StateSerializer(many=False, source='get_state')

    class Meta:
        model = UtilityState
        fields = ('id_string', 'label', 'state')