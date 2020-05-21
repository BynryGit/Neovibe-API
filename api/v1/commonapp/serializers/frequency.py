__author__ = "priyanka"

from rest_framework import serializers
from v1.commonapp.models.frequency import Frequency

class FrequencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Frequency
        fields = ('id_string', 'name')