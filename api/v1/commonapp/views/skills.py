__author__ = "Priyanka"

from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.skills import Skills
from v1.commonapp.serializers.skill import GetSkillSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.utility.models.utility_master import get_utility_by_id_string


class SkillsList(generics.ListAPIView):
    try:
        serializer_class = GetSkillSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = Skills.objects.filter(utility = utility, is_active = True)

                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Skill not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Commonapp', sub_module = 'Commonapp')
