from rest_framework import serializers
from v1.consumer.models.offer_type import OfferType


class OfferTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferType
        fields = ('name', 'id_string', 'created_date', 'is_active', 'created_by')


