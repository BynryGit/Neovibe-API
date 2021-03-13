__author__ = "aki"

from rest_framework import serializers


class AssignRevisitTaskAssignmentViewSerializer(serializers.Serializer):
    route_task_assignment_id_staring = serializers.UUIDField(required=True)
    meter_no = serializers.CharField(required=True)
    consumer_no = serializers.CharField(required=True)
    meter_reader_id_string = serializers.UUIDField(required=True)
