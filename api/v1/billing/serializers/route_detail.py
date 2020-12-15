from rest_framework import serializers
from v1.billing.models.route_detail import RouteDetail


class RouteDetailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteDetail
        fields = ('route_detail_id_string', 'route_code', 'bill_month')