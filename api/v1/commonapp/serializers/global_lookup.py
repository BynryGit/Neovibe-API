from rest_framework import serializers
from v1.commonapp.models.global_lookup import Global_Lookup as Global_LookupTbl


class GlobalLookupShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Global_LookupTbl
        fields = ('id_string', 'value')