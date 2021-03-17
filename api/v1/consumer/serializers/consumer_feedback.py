from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_feedback import ConsumerFeedback
from v1.consumer.views import common_functions
from v1.utility.models.contact_us import ContactUs


class ConsumerFeedbackListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerFeedback
        fields = ('tenant', 'tenant_id_string', 'utility', 'utility_id_string', "feedback")


class ConsumerFeedbackSerializer(serializers.ModelSerializer):
    utility = serializers.CharField(required=False, max_length=200)
    consumer_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ConsumerFeedback
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = common_functions.set_consumer_feedback_validated_data(validated_data)
        with transaction.atomic():
            obj = super(ConsumerFeedbackSerializer, self).create(validated_data)
            obj.tenant = user.tenant
            obj.created_by = user.id
            obj.created_date = datetime.now()
            obj.is_active = True
            obj.save()
            return obj
