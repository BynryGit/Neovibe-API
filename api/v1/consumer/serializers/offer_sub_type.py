from rest_framework import serializers
from v1.consumer.models.offer_sub_type import OfferSubType
from v1.consumer.serializers.offer_type import OfferTypeListSerializer


class OfferSubTypeListSerializer(serializers.ModelSerializer):
    offer_type = OfferTypeListSerializer(source='get_offer_type')

    class Meta:
        model = OfferSubType
        fields = ('name', 'id_string', 'offer_type', 'created_date', 'is_active', 'created_by')


