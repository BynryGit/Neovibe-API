from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from v1.payment.models.consumer_payment import Payment
from v1.payment.serializer.payment_channel import PaymentChannelListSerializer
from v1.payment.serializer.payment_mode import PaymentModeListSerializer
from v1.payment.serializer.payment_sub_type import PaymentSubTypeListSerializer
from v1.payment.serializer.payment_type import PaymentTypeListSerializer
from v1.payment.views.common_functions import set_validated_data


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


class PaymentListSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeListSerializer(many=False, source='get_payment_type')
    payment_sub_type = PaymentSubTypeListSerializer(many=False, source='get_payment_sub_type')
    payment_mode = PaymentModeListSerializer(many=False, source='get_payment_mode')
    payment_channel = PaymentChannelListSerializer(many=False, source='get_payment_channel')

    class Meta:
        model = Payment
        fields = ('id_string', 'state', 'transaction_amount', 'transaction_charges', 'payment_type', 'payment_sub_type', 'payment_mode', 'payment_channel')


class PaymentViewSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeListSerializer(many=False, source='get_payment_type')
    payment_sub_type = PaymentSubTypeListSerializer(many=False, source='get_payment_sub_type')
    payment_mode = PaymentModeListSerializer(many=False, source='get_payment_mode')
    payment_channel = PaymentChannelListSerializer(many=False, source='get_payment_channel')
    state = ChoiceField(choices=Payment.CHOICES)

    class Meta:
        model = Payment
        fields = ('id_string', 'transaction_amount', 'transaction_charges', 'state', 'payment_type', 'payment_sub_type', 'payment_mode', 'payment_channel')


class PaymentSerializer(serializers.ModelSerializer):
    payment_type_id = serializers.CharField(required=False, max_length=200)
    payment_sub_type_id = serializers.CharField(required=False, max_length=200)
    payment_mode_id = serializers.CharField(required=False, max_length=200)
    payment_channel_id = serializers.CharField(required=False, max_length=200)
    payment_source_id = serializers.CharField(required=False, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Payment
        fields = ('__all__')

    def create(self, validated_data, user, obj):
        validated_data =  set_validated_data(validated_data)
        with transaction.atomic():
            payment = super(PaymentSerializer, self).create(validated_data)
            payment.created_by = user.id
            payment.created_date = datetime.utcnow()
            payment.tenant = user.tenant
            payment.utility.id = validated_data['utility_id']
            payment.identification_id = obj.id
            payment.save()
        return payment

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            payment = super(PaymentSerializer, self).update(instance, validated_data)
            payment.updated_by = user.id
            payment.updated_date = datetime.utcnow()
            payment.save()
        return payment