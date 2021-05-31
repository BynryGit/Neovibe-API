__author__ = "chinmay"

from django.db import transaction
from django.utils import timezone
# from api.messages import VALIDATION_ASSIGNMENT_ALREADY_EXISTS
from rest_framework import serializers, status
from api.messages import *
from django.db import transaction
from v1.meter_data_management.models.validation_assignments import \
    ValidationAssignment as ValidationAssignmentTbl
from v1.meter_data_management.views.common_function import set_validation_assignment_validated_data
from v1.userapp.serializers.user import GetUserSerializer
from v1.meter_data_management.serializers.read_cycle import ReadCycleListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from datetime import datetime


class ValidationAssignmentListSerializer(serializers.ModelSerializer):
    validator1 = GetUserSerializer(source='get_validator_1')
    validator2 = GetUserSerializer(source='get_validator_2')
    read_cycle = ReadCycleListSerializer(source='get_read_cycle')

    class Meta:
        model = ValidationAssignmentTbl
        fields = ('id_string', 'validator1', 'validator2', 'read_cycle', 'created_date', 'is_active', 'created_by')


class ValidationAssignmentViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ValidationAssignmentTbl
        fields = ('id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class ValidationAssignmentSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=False)
    tenant_id = serializers.UUIDField(required=False)
    validator1_id = serializers.UUIDField(required=True)
    validator2_id = serializers.UUIDField(required=True)
    read_cycle_id = serializers.UUIDField(required=False)



    class Meta:
        model = ValidationAssignmentTbl
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_validation_assignment_validated_data(validated_data)
        if ValidationAssignmentTbl.objects.filter(tenant_id=validated_data['tenant_id'],
                                                  utility_id=validated_data['utility_id'],
                                                  read_cycle_id=validated_data['read_cycle_id'],validator1_id=validated_data['validator1_id'],
                                                  validator2_id=validated_data['validator2_id']).exists():
            raise CustomAPIException(SMART_METER_CONFIGURATION_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                validation_obj = super(ValidationAssignmentSerializer, self).create(validated_data)
                validation_obj.tenant = user.tenant
                validation_obj.created_by = user.id
                validation_obj.save()
                return validation_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validation_assignment_validated_data(validated_data)
        if ValidationAssignmentTbl.objects.filter(tenant_id=validated_data['tenant_id'],
                                                  utility_id=validated_data['utility_id'],
                                                  read_cycle_id=validated_data['read_cycle_id'],validator1_id=validated_data['validator1_id'],
                                                  validator2_id=validated_data['validator2_id']).exists():
            raise CustomAPIException(SMART_METER_CONFIGURATION_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                validation_obj = super(ValidationAssignmentSerializer, self).update(instance, validated_data)
                validation_obj.tenant = user.tenant
                validation_obj.updated_by = user.id
                validation_obj.updated_date = timezone.now()
                validation_obj.save()
                return validation_obj
