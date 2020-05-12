from rest_framework import serializers

from v1.commonapp.models.city import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'id_string')