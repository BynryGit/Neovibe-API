from rest_framework import serializers
from v1.survey.models.survey_subtype import SurveySubType as SurveySubTypeTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import SURVEY_SUBTYPE_ALREADY_EXIST
from v1.survey.views.common_functions import set_survey_subtype_validated_data
from rest_framework import status
from v1.survey.models.survey_type import get_survey_type_by_id_string
from v1.survey.serializers.survey_type import SurveyTypeListSerializer

class SurveySubTypeListSerializer(serializers.ModelSerializer):
    survey_type = SurveyTypeListSerializer(many="False", source='get_survey_type')
    class Meta:
        model = SurveySubTypeTbl
        fields = ('name', 'id_string','survey_type','created_date','is_active','created_by')

class SurveySubTypeViewSerializer(serializers.ModelSerializer):
    

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = SurveySubTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string','created_date')

class SurveySubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    survey_type_id = serializers.CharField(required=True, max_length=200)
    

    class Meta:
        model = SurveySubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_survey_subtype_validated_data(validated_data)
            if SurveySubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SURVEY_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                survey_subtype_obj = super(SurveySubTypeSerializer, self).create(validated_data)
                survey_subtype_obj.created_by = user.id
                survey_subtype_obj.updated_by = user.id
                survey_subtype_obj.save()
                return survey_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_survey_subtype_validated_data(validated_data)
        with transaction.atomic():
            survey_subtype_obj = super(SurveySubTypeSerializer, self).update(instance, validated_data)
            survey_subtype_obj.updated_by = user.id
            survey_subtype_obj.updated_date = datetime.utcnow()
            survey_subtype_obj.save()
            return survey_subtype_obj