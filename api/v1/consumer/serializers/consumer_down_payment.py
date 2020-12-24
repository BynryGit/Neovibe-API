from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_down_payment import ConsumerDownPayment


class ConsumerDownPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerDownPayment
        fields = '__all__'

    def create(self, validated_data, consumer_obj, user):
        with transaction.atomic():
            consumer_down_payment = super(ConsumerDownPaymentSerializer, self).create(validated_data=validated_data)
            consumer_down_payment.tenant = consumer_obj.tenant
            consumer_down_payment.utility = consumer_obj.utility
            consumer_down_payment.consumer_id = consumer_obj.id
            consumer_down_payment.created_by = user.id
            consumer_down_payment.created_date = datetime.now()
            return consumer_down_payment
