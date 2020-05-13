import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from v1.commonapp.models.skills import get_skills_by_utility_id_string
from v1.userapp.serializers.skills import SkillListSerializer



# API Header
# API end Point: api/v1/user/skill
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View skill list
# Usage: This will get all skills according to utility.
# Tables used: 2.12.76. Lookup - Skills
# Author: Arpita
# Created on: 13/05/2020


class SkillList(generics.ListAPIView):
    serializer_class = SkillListSerializer

    def get_queryset(self):

        queryset = get_skills_by_utility_id_string(1)
        return queryset
