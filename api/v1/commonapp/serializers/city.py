from rest_framework import serializers

from v1.commonapp.models.city import City as CityTbl


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CityTbl
        fields = ('id_string', 'name')