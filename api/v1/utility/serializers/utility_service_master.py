from rest_framework import serializers
from v1.utility.models.utility_service_master import UtilityServiceMaster


class UtilityServiceMasterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UtilityServiceMaster
        fields = ('id_string', 'service_name')