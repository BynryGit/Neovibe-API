from rest_framework import serializers
from v1.consumer.models.source_type import SourceType


class SourceTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceType
        fields = ('name', 'id_string')


class SourceTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SourceType
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')