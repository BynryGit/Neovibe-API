__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.serializers.module import CustomModuleShortViewSerializer
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl


class UtilityModuleSubmoduleViewSerializer(serializers.ModelSerializer):
    module = CustomModuleShortViewSerializer(many=False, source='get_module')

    class Meta:
        model = UtilityModuleTbl
        fields = ('module',)
