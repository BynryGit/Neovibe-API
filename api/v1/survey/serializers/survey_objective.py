from rest_framework import serializers
from v1.survey.models.survey_objective import SurveyObjective
from api.settings import DISPLAY_DATE_TIME_FORMAT

class SurveyObjectiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyObjective
        fields = ('objective','id_string')

class SurveyObjectiveViewSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = SurveyObjective
        fields = ('id_string', 'objective', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')