__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.models.state import State as StateTbl
from v1.consumer.views.common_functions import set_validated_data
from django.db import transaction


class StateSerializer(serializers.ModelSerializer):
    # utility_id = serializers.CharField(required=False, max_length=200)
    # tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = StateTbl
        fields = ('__all__')
    
    # def create(self, validated_data, user):
    #     validated_data =  set_validated_data(validated_data)
    #     with transaction.atomic():
    #         state_obj = super(StateSerializer, self).create(validated_data)
    #         state_obj.created_by = user.id
    #         state_obj.save()
    #         return state_obj


class StateViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = StateTbl
        fields = ('__all__')

class StateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StateTbl
        fields = ('name', 'id_string','key')

