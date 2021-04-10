__author__ = "aki"

from rest_framework import serializers, status
from v1.commonapp.models.state import State as StateTbl
from v1.commonapp.serializers.country import CountryListSerializer
from v1.commonapp.common_functions import set_state_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import STATE_ALREADY_EXIST
from datetime import datetime
from django.db import transaction


class StateShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateTbl
        fields = ('id_string', 'name')


class StateViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = StateTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class StateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    country_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = StateTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_state_validated_data(validated_data)
            if StateTbl.objects.filter(name=validated_data['name'],country_id=validated_data['country_id'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(STATE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                state_obj = super(StateSerializer, self).create(validated_data)
                state_obj.created_by = user.id
                state_obj.save()
                return state_obj

    def update(self, instance, validated_data, user):
        validated_data = set_state_validated_data(validated_data)
        if StateTbl.objects.filter(name=validated_data['name'],country_id=validated_data['country_id'], tenant_id=validated_data['tenant_id'],
                                   utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(STATE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                state_obj = super(StateSerializer, self).update(instance, validated_data)
                state_obj.updated_by = user.id
                state_obj.updated_date = datetime.utcnow()
                state_obj.save()
                return state_obj


class StateListSerializer(serializers.ModelSerializer):
    country_id = CountryListSerializer(source="get_country")

    class Meta:
        model = StateTbl
        fields = ('name', 'id_string', 'country_id','created_date','is_active','created_by')
