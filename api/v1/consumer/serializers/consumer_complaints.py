from rest_framework import serializers
from v1.consumer.models.consumer_complaints import ConsumerComplaints


class ConsumerComplaintListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerComplaints
        fields = ('name', 'id_string')


class ConsumerComplaintViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerComplaints
        fields = ('__all__')