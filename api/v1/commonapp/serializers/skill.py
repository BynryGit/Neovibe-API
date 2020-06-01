from rest_framework import serializers
from v1.commonapp.models.skills import Skills


class GetSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ('skill', 'id_string')