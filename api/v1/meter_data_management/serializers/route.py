from rest_framework import serializers, status
from django.db import transaction
from v1.meter_data_management.views.common_function import set_route_validated_data
from datetime import datetime
from api.messages import ROUTE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.route import Route as RouteTbl


class RouteViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = RouteTbl
        fields = ('name', 'id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class RouteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = RouteTbl
        fields = ('name', 'id_string', 'utility_id', 'tenant_id', 'premises_json', 'filter_json')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_route_validated_data(validated_data)
            if RouteTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(ROUTE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                route_obj = super(RouteSerializer, self).create(validated_data)
                route_obj.created_by = user.id
                route_obj.updated_by = user.id
                route_obj.save()
                return route_obj

    def update(self, instance, validated_data, user):
        validated_data = set_route_validated_data(validated_data)
        with transaction.atomic():
            route_obj = super(RouteSerializer, self).update(instance, validated_data)
            route_obj.tenant = user.tenant
            route_obj.updated_by = user.id
            route_obj.updated_date = datetime.utcnow()
            route_obj.save()
            return route_obj


class RouteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTbl
        fields = '__all__'


class RouteShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTbl
        fields = ('id_string','name')