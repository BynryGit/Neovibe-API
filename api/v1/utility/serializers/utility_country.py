from rest_framework import serializers
from v1.commonapp.serializers.country import CountrySerializer
from v1.utility.models.utility_country import UtilityCountry


class UtilityCountryListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False, source='get_country')

    class Meta:
        model = UtilityCountry
        fields = ('id_string', 'label', 'country')