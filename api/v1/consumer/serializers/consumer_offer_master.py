from rest_framework import serializers
from v1.consumer.models.consumer_offer_master import ConsumerOfferMaster
from v1.consumer.serializers.offer_sub_type import OfferSubTypeListSerializer


class ConsumerOfferMasterListSerializer(serializers.ModelSerializer):
    offer_sub_type = OfferSubTypeListSerializer(source='get_offer_sub_type')

    class Meta:
        model = ConsumerOfferMaster
        fields = ('offer_name', 'id_string', 'offer_code', 'offer_sub_type')

