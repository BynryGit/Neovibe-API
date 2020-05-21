from rest_framework import serializers
from v1.consumer.models.consumer_services import ServiceDetails


class ServiceDetailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceDetails
        fields = ('name', 'id_string', 'request_date')


class ServiceDetailViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ServiceDetails
        fields = ('__all__')