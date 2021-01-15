from rest_framework import serializers
from v1.commonapp.models.global_lookup import Global_Lookup as Global_LookupTbl


class GlobalLookupShortViewSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    def get_value(self, global_lookup_tbl):
        if global_lookup_tbl:
            value = global_lookup_tbl.value
        else:
            value= 'None'
        return value

    class Meta:
        model = Global_LookupTbl
        fields = ('id_string', 'value')


class GlobalLookupViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Global_LookupTbl
        fields = ('__all__')