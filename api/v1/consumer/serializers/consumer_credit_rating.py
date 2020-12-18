from rest_framework import serializers
from v1.consumer.models.consumer_credit_rating import ConsumerCreditRating


class ConsumerCreditRatingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerCreditRating
        fields = ('rating', 'id_string')

