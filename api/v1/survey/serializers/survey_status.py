from rest_framework import serializers
from v1.survey.models.survey_status import SurveyStatus

class SurveyStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyStatus
        fields = ('name','id_string')

class SurveyStatusViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SurveyStatus
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')