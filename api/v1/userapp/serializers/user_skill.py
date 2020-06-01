from rest_framework import serializers

from v1.commonapp.serializers.skill import GetSkillSerializer
from v1.userapp.models.user_skill import UserSkill


class UserSkillSerializer(serializers.ModelSerializer):
    skill = GetSkillSerializer(many=False, required=True, source='get_skill')

    class Meta:
        model = UserSkill
        fields = ('skill',)
