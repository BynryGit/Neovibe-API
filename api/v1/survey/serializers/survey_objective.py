from rest_framework import serializers, status
from v1.survey.models.survey_objective import SurveyObjective as SurveyObjectiveTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import SURVEY_OBJECTIVE_ALREADY_EXIST
from v1.survey.serializers.survey_type import SurveyTypeListSerializer
from v1.survey.serializers.survey_subtype import SurveySubTypeListSerializer
from v1.survey.views.common_functions import set_survey_objective_validated_data
from django.db import transaction
from datetime import datetime


class SurveyObjectiveListSerializer(serializers.ModelSerializer):
    survey_type = SurveyTypeListSerializer(many="False", source='get_survey_type')
    survey_subtype = SurveySubTypeListSerializer(many="False", source='get_survey_subtype')
    class Meta:
        model = SurveyObjectiveTbl
        fields = ('objective','id_string','survey_type','survey_subtype','created_date','is_active','created_by')

class SurveyObjectiveViewSerializer(serializers.ModelSerializer):
    # def get_created_date(self, obj):
    #     return obj.created_date.strftime(setting_reader.get_display_date_format())

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = SurveyObjectiveTbl
        fields = ('id_string', 'objective', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')


class SurveyObjectiveSerializer(serializers.ModelSerializer):
    objective = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Objective is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    survey_type_id = serializers.CharField(required=True, max_length=200)
    survey_subtype_id = serializers.CharField(required=True, max_length=200)
    

    class Meta:
        model = SurveyObjectiveTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_survey_objective_validated_data(validated_data)
            if SurveyObjectiveTbl.objects.filter(objective=validated_data['objective'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SURVEY_OBJECTIVE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                survey_obj = super(SurveyObjectiveSerializer, self).create(validated_data)
                survey_obj.created_by = user.id
                survey_obj.updated_by = user.id
                survey_obj.save()
                return survey_obj

    def update(self, instance, validated_data, user):
        validated_data = set_survey_objective_validated_data(validated_data)
        with transaction.atomic():
            survey_obj = super(SurveyObjectiveSerializer, self).update(instance, validated_data)
            survey_obj.updated_by = user.id
            survey_obj.updated_date = datetime.utcnow()
            survey_obj.save()
            return survey_obj