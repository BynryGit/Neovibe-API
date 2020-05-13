__author__ = "Priyanka"

from rest_framework import serializers
from v1.survey.models.survey import Survey as SurveyTbl
from v1.survey.models.survey_status import SurveyStatus
from v1.survey.models.survey_type import SurveyType
from v1.survey.models.survey_objective import SurveyObjective

class SurveyObjectiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyObjective
        fields = ('objective','id_string')

class SurveyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyType
        fields = ('name','id_string')

class SurveyStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyStatus
        fields = ('name','id_string')

class SurveyListSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    objective = SurveyObjectiveSerializer(many=False,required=True,source='get_objective')
    type = SurveyTypeSerializer(many=False,required=True,source='get_type')
    status = SurveyStatusSerializer(many=False,required=True,source='get_status')

    class Meta:
        model = SurveyTbl
        fields = ('id_string', 'tenant_name', 'name', 'description','start_date','end_date','no_of_consumers',
                  'category_id','sub_category_id','area_id','sub_area_id',
                  'completion_date','objective','type','status')

class SurveyViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    objective = SurveyObjectiveSerializer(many=False, required=True, source='get_objective')
    type = SurveyTypeSerializer(many=False, required=True, source='get_type')
    status = SurveyStatusSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = SurveyTbl
        fields = ('id_string', 'tenant_name', 'name', 'description', 'start_date', 'end_date', 'no_of_consumers',
                  'category_id', 'sub_category_id', 'area_id', 'sub_area_id',
                  'completion_date', 'objective', 'type', 'status')

