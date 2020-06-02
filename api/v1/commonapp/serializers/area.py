from rest_framework import serializers
from v1.commonapp.models.area import Area


class GetAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('name', 'id_string')


class AreaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('name', 'id_string')


class AreaViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = Area
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')