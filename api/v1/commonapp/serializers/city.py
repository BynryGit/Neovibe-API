from rest_framework import serializers
from v1.commonapp.models.city import City as CityTbl
from rest_framework import serializers, status
from v1.commonapp.serializers.state import StateListSerializer, StateViewSerializer
from api.messages import CITY_ALREADY_EXIST
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_city_validated_data


class CityShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityTbl
        fields = ('id_string', 'name')


class CityViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = CityTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class CitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = CityTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_city_validated_data(validated_data)
            if CityTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                      utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CITY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                city_obj = super(CitySerializer, self).create(validated_data)
                city_obj.created_by = user.id
                city_obj.updated_by = user.id
                city_obj.save()
                return city_obj

    def update(self, instance, validated_data, user):
        validated_data = set_city_validated_data(validated_data)
        with transaction.atomic():
            city_obj = super(CitySerializer, self).update(instance, validated_data)
            city_obj.updated_by = user.id
            city_obj.updated_date = datetime.utcnow()
            city_obj.save()
            return city_obj


class CityListSerializer(serializers.ModelSerializer):
    state = StateListSerializer(source="get_state")

    class Meta:
        model = CityTbl
        fields = ('name', 'id_string', 'state', 'is_active', 'created_by', 'created_date')
