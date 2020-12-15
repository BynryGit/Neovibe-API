from rest_framework import serializers
from v1.complaint.models.complaint_assignment import ComplaintAssignment


class ComplaintAssignmentListSerializer(serializers.ModelSerializer):
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    complaint_name = serializers.ReadOnlyField(source='get_complaint_name')
    complaint_id_string = serializers.ReadOnlyField(source='get_complaint_id_string')

    class Meta:
        model = ComplaintAssignment
        fields = ('tenant_id_string', 'utility_id_string', 'complaint_name', 'complaint_id_string')