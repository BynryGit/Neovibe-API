from rest_framework import serializers
from v1.commonapp.serializers.currency import CurrencySerializer
from v1.utility.models.utility_currency import UtilityCurrency


class UtilityCurrencyListSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, source='get_currency')

    class Meta:
        model = UtilityCurrency
        fields = ('id_string', 'label', 'currency')
