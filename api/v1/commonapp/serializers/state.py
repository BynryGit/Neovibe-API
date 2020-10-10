__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.models.state import State as StateTbl


class StateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StateTbl
        fields = ('id_string', 'name')