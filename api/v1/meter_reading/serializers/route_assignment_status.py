__author__ = "aki"

from rest_framework import serializers
from v1.meter_reading.models.route_assignment_status import RouteAssignmentStatus as RouteAssignmentStatusTbl


class RouteAssignmentStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteAssignmentStatusTbl
        fields = ('id_string', 'name')