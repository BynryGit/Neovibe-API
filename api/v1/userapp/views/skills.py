import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from api.constants import *
from v1.commonapp.models.skills import get_skills_by_utility_id_string
from v1.userapp.serializers.skills import SkillListSerializer
from v1.userapp.decorators import is_token_validate, role_required


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

    @is_token_validate
    @role_required(ADMIN, UTILITY_MASTER, EDIT)
    def get_queryset(self):
        queryset = get_skills_by_utility_id_string(1)
        return queryset
