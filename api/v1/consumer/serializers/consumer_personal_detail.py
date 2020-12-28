from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_personal_detail import ConsumerPersonalDetail


class ConsumerPersonalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerPersonalDetail
        fields = '__all__'

    def create(self, validated_data, consumer_obj, user):
        with transaction.atomic():
            consumer_personal_detail = super(ConsumerPersonalDetailSerializer, self).create(validated_data=validated_data)
            consumer_personal_detail.tenant = consumer_obj.tenant
            consumer_personal_detail.utility = consumer_obj.utility
            consumer_personal_detail.consumer_id = consumer_obj.id
            consumer_personal_detail.consumer_no = consumer_obj.consumer_no
            consumer_personal_detail.created_by = user.id
            consumer_personal_detail.created_date = datetime.now()
            consumer_personal_detail.is_active = True
            consumer_personal_detail.save()
            return consumer_personal_detail
