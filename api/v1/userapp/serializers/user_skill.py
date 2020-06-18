from datetime import datetime
from django.db import transaction
from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.skill import GetSkillSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_skill import UserSkill
from v1.userapp.views.common_functions import set_user_skill_validated_data


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

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserSkill
        fields = ('id_string', 'tenant', 'created_date')


class UserSkillSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    skill_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserSkill
        fields = '__all__'

    def create(self, validate_data, user):
        validated_data = set_user_skill_validated_data(validate_data)
        if UserSkill.objects.filter(user_id=validated_data['user_id'], skill_id=validated_data['skill_id'],
                                        tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Skill already exists for specified user!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_skill_obj = super(UserSkillSerializer, self).create(validated_data)
                user_skill_obj.created_by = user.id
                user_skill_obj.updated_by = user.id
                user_skill_obj.created_date = datetime.utcnow()
                user_skill_obj.updated_date = datetime.utcnow()
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


