__author__ = "Priyanka"

from rest_framework import serializers
from v1.survey.models.survey_consumer import SurveyConsumer


class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    class Meta:
        model = SurveyConsumer
        fields = ('tenant_name','consumer_no','first_name','middle_name','last_name','email_id','phone_mobile',
                  'address_line_1')

class ConsumerListSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    survey = serializers.ReadOnlyField(source='get_survey')

    class Meta:
        model = SurveyConsumer
        fields = ('survey','tenant_name','consumer_no', 'first_name', 'middle_name', 'last_name', 'email_id', 'phone_mobile',
                  'address_line_1')