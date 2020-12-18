from rest_framework import serializers
from v1.consumer.models.consumer_offer_master import ConsumerOfferMaster


class ConsumerOfferMasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerOfferMaster
        fields = ('offer_name', 'id_string')

