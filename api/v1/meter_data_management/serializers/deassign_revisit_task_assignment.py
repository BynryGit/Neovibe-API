__author__ = "aki"

from rest_framework import serializers


class DeAssignRevisitTaskAssignmentViewSerializer(serializers.Serializer):
    route_task_assignment_id_staring = serializers.UUIDField(required=True)
    meter_no = serializers.CharField(required=True)
    consumer_no = serializers.CharField(required=True)
