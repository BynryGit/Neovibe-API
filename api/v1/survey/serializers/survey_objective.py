from rest_framework import serializers
from v1.survey.models.survey_objective import SurveyObjective

class SurveyObjectiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyObjective
        fields = ('objective','id_string')

class SurveyObjectiveViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SurveyObjective
        fields = ('id_string', 'objective', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')