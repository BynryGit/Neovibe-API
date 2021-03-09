from api.messages import CONSUMER_FAQ_ALREADY_EXIST
from rest_framework import status
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryListSerializer
from v1.consumer.serializers.consumer_category import ConsumerCategoryListSerializer
from v1.consumer.models.consumer_faq import ConsumerFaq as ConsumerFaqTbl
from rest_framework import serializers
from v1.commonapp.views.custom_exception import CustomAPIException
from django.db import transaction
from datetime import datetime

from v1.consumer.views.common_functions import set_consumer_faq_validated_data


class ConsumerFaqListSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConsumerFaqTbl
            fields = (
                'question', 'answer', 'id_string', 'created_date', 'is_active',
                'created_by')


class ConsumerFaqViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerFaqTbl
        fields = ('id_string', 'question','answer', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date')


class ConsumerFaqSerializer(serializers.ModelSerializer):
    question = serializers.CharField(required=True, max_length=200,
                                     error_messages={"required": "The field question is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)


    class Meta:
        model = ConsumerFaqTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_faq_validated_data(validated_data)
            if ConsumerFaqTbl.objects.filter(question=validated_data['question'], tenant_id=validated_data['tenant_id'],
                                             utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CONSUMER_FAQ_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_faq_obj = super(ConsumerFaqSerializer, self).create(validated_data)
                consumer_faq_obj.created_by = user.id
                consumer_faq_obj.save()
                return consumer_faq_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_faq_validated_data(validated_data)
        if ConsumerFaqTbl.objects.filter(question=validated_data['question'], tenant_id=validated_data['tenant_id'],
                                         utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(CONSUMER_FAQ_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                consumer_faq_obj = super(ConsumerFaqSerializer, self).update(instance, validated_data)
                consumer_faq_obj.updated_by = user.id
                consumer_faq_obj.updated_date = datetime.utcnow()
                consumer_faq_obj.save()
                return consumer_faq_obj
