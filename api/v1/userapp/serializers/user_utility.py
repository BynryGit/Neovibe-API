from rest_framework import serializers

from v1.userapp.models.user_utility import UserUtility
from v1.utility.serializers.utility import UtilitySerializer


class UserUtilitySerializer(serializers.ModelSerializer):
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserUtility
        fields = ('utility',)
