import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from v1.commonapp.models.area import get_areas_by_utility_id_string
from v1.commonapp.models.skills import get_skills_by_utility_id_string
from v1.userapp.serializers.area import AreaListSerializer


# API Header
# API end Point: api/v1/user/area
# API verb: GET
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: View skill area
# Usage: This will get all area according to utility.
# Tables used: 2.12.8. Lookup - Area
# Author: Arpita
# Created on: 13/05/2020


class AreaList(generics.ListAPIView):
    serializer_class = AreaListSerializer

    def get_queryset(self):

        queryset = get_areas_by_utility_id_string(1)
        return queryset
