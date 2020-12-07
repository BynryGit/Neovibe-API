__author__ = "aki"

from rest_framework import serializers
from v1.meter_data_management.models.route_upload_status import RouteUploadStatus as RouteUploadStatusTbl


class RouteUploadStatusShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteUploadStatusTbl
        fields = ('id_string', 'name')