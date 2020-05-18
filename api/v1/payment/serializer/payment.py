from rest_framework import serializers
from v1.payment.models.consumer_payment import ConsumerPayment
from v1.payment.views.common_functions import set_validated_data


class PaymentSerializer(serializers.ModelSerializer):
    payment_type = serializers.CharField(required=False, max_length=200)
    payment_subtype = serializers.CharField(required=False, max_length=200)
    payment_mode = serializers.CharField(required=False, max_length=200)
    payment_channel = serializers.CharField(required=False, max_length=200)
    payment_provider = serializers.CharField(required=False, max_length=200)


    class Meta:
        model = ConsumerPayment
        fields = ('__all__')

    def create(self, validated_data, user, obj):
        validated_data =  set_validated_data(validated_data)

    def update(self, instance, validated_data, user):
        pass