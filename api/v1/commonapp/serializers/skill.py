from rest_framework import serializers, status
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.models.skills import Skills as SkillTbl
from v1.commonapp.serializers.service_type import GetServiceTypeSerializer
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer
from api.messages import SKILL_ALREADY_EXIST
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_skill_validated_data
from django.db import transaction

class GetSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model =  SkillTbl
        fields = ('skill', 'id_string')


class SkillViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SkillTbl
        fields = ('id_string', 'skill', 'description', 'created_date', 'updated_date', 'tenant', 'utility','tenant_id_string','utility_id_string')

class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTbl
        fields = ('id_string', 'skill')

class SkillSerializer(serializers.ModelSerializer):
    skill = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field Skill is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    

    class Meta:
        model = SkillTbl
        fields = '__all__'
    
    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_skill_validated_data(validated_data)
            if SkillTbl.objects.filter(skill=validated_data['skill'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SKILL_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                skill_obj = super(SkillSerializer, self).create(validated_data)
                skill_obj.created_by = user.id
                skill_obj.updated_by = user.id
                skill_obj.save()
                return skill_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            validated_data = set_skill_validated_data(validated_data)
            if SkillTbl.objects.filter(skill=validated_data['skill'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SKILL_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            skill_obj = super(SkillSerializer, self).update(instance, validated_data)
            skill_obj.updated_by = user.id
            skill_obj.updated_date = datetime.utcnow()
            skill_obj.save()
            return skill_obj
