__author__ = "aki"

from rest_framework import serializers
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl


class UtilityMasterViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = UtilityMasterTbl
        fields = ('id_string', 'name')