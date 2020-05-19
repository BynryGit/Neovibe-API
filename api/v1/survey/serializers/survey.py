__author__ = "Priyanka"
from django.db import transaction
from datetime import datetime
from rest_framework import serializers
from v1.survey.models.survey import Survey as SurveyTbl
from v1.survey.models.survey_status import SurveyStatus
from v1.survey.models.survey_type import SurveyType
from v1.survey.models.survey_objective import SurveyObjective
from v1.survey.views.common_functions import set_survey_validate_data

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
    objective_id = SurveyObjectiveSerializer(many=False, required=True, source='get_objective')
    type_id = SurveyTypeSerializer(many=False, required=True, source='get_type')
    status_id = SurveyStatusSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = SurveyTbl
        fields = ('id_string', 'tenant_name', 'name', 'description', 'start_date', 'end_date', 'no_of_consumers',
                  'category_id', 'sub_category_id', 'area_id', 'sub_area_id',
                  'completion_date', 'objective_id', 'type_id', 'status_id')

class SurveySerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    name = serializers.CharField(required=False, max_length=200)
    objective_id = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    type_id = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)
    no_of_consumers = serializers.CharField(required=False, max_length=200)
    completion_date = serializers.CharField(required=False, max_length=200)
    start_date = serializers.CharField(required=False, max_length=200)
    end_date = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = SurveyTbl
        fields = ('id_string', 'tenant_name', 'name', 'description', 'start_date', 'end_date', 'no_of_consumers',
                  'category_id', 'sub_category_id', 'area_id', 'sub_area_id',
                  'completion_date', 'objective_id', 'type_id', 'status_id')

    def create(self, validated_data, user):
        validated_data = set_survey_validate_data(validated_data)
        with transaction.atomic():
            survey_obj = super(SurveySerializer, self).create(validated_data)
            survey_obj.created_by = user.id
            survey_obj.created_date = datetime.now()
            survey_obj.save()
            return survey_obj

    def update(self, instance, validated_data, user):
        validated_data = set_survey_validate_data(validated_data)
        with transaction.atomic():
            survey_obj = super(SurveySerializer, self).update(instance, validated_data)
            survey_obj.updated_by = user.id
            survey_obj.updated_date = datetime.now()
            survey_obj.save()
            return survey_obj

