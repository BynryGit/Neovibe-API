from rest_framework import serializers
from v1.complaint.models.complaint_type import ComplaintType


class ComplaintTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplaintType
        fields = ('name', 'id_string')


class ComplaintTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ComplaintType
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')