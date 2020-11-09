from rest_framework import serializers
from v1.commonapp.models.currency import Currency


class CurrencyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id_string', 'name', 'key')


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('__all__')