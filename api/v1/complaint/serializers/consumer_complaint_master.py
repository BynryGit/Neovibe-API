from rest_framework import serializers
from v1.complaint.models.consumer_complaint_master import ConsumerComplaintMaster
from v1.complaint.serializers.complaint_subtype import ComplaintSubTypeListSerializer


class ConsumerComplaintMasterListSerializer(serializers.ModelSerializer):
    complaint_sub_type = ComplaintSubTypeListSerializer(source='get_complaint_sub_type')

    class Meta:
        model = ConsumerComplaintMaster
        fields = ('id_string', 'name', 'complaint_sub_type')
