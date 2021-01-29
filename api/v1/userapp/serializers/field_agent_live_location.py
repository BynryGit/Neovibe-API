from django.db import transaction
from datetime import datetime
from v1.userapp.serializers.user import GetUserSerializer
from rest_framework import serializers, status

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.userapp.models.user_utility import UserUtility
from v1.userapp.views.common_functions import set_user_utility_validated_data
from v1.utility.serializers.utility import UtilitySerializer
from v1.userapp.models.field_agent_live_location import FieldAgentLiveLocation

class FieldAgentLiveLocationViewSerializer(serializers.ModelSerializer):

    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    user_id = GetUserSerializer(many=False, required=True, source='get_user')
    class Meta:
        model = FieldAgentLiveLocation
        fields = ('__all__')
