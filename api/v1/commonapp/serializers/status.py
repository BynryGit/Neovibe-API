from rest_framework import serializers

from v1.utility.models.utility_status import UtilityStatus as UtilityStatusTbl


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UtilityStatusTbl
        fields = ('id_string', 'status')