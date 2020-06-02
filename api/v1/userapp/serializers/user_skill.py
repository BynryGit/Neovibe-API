from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.skill import GetSkillSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.user_skill import UserSkill


class GetUserSkillSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    skill = GetSkillSerializer(many=False, required=True, source='get_skill')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserSkill
        fields = ('id_string', 'skill',)


class UserSkillViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserSkill
        fields = ('id_string', 'tenant', 'created_date')


class UserSkillSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    skill_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = UserSkill
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            user_skill_obj = super(UserSkillSerializer, self).create(validated_data)
            user_skill_obj.created_by = user.id
            user_skill_obj.created_date = datetime.utcnow()
            user_skill_obj.tenant = user.tenant
            user_skill_obj.is_active = True
            user_skill_obj.save()
            return user_skill_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            user_skill_obj = super(UserSkillSerializer, self).update(instance, validated_data)
            user_skill_obj.updated_by = user.id
            user_skill_obj.updated_date = datetime.utcnow()
            user_skill_obj.is_active = True
            user_skill_obj.save()
            return user_skill_obj


