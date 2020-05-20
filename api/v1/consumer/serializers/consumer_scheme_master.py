from rest_framework import serializers

from v1.consumer.models.consumer_scheme_master import ConsumerSchemeMaster


class ConsumerSchemeMasterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerSchemeMaster
        fields = ('scheme_name', 'id_string')


class ConsumerSchemeMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerSchemeMaster
        fields = ('id_string', 'scheme_name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')