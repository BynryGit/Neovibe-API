__author__ = "Priyanka"
from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status
import random
from rest_framework.validators import UniqueTogetherValidator
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.work_order.models.service_assignment import ServiceAssignment
from v1.work_order.views.common_functions import set_service_assignment_validated_data
from api.messages import SERVICE_ASSIGNMENT_ALREADY_EXIST
from v1.work_order.serializers.service_appointment import ServiceAppointmentViewSerializer
from v1.userapp.serializers.user import GetUserSerializer
from v1.tenant.serializers.tenant import TenantStatusViewSerializer
from v1.work_order.serializers.service_appointment_status import ServiceAppointmentStatusListSerializer
from v1.commonapp.views.custom_exception import CustomAPIException


class ServiceAssignmentListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    sa_id = ServiceAppointmentViewSerializer(many=False, required=True, source='get_service_appointment')
    user_id = GetUserSerializer(many=False, required=True, source='get_user')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = ServiceAssignment
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'sa_id', 'user_id',
                  'created_date', 'updated_date','assignment_date','completion_date')

class ServiceAssignmentSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    sa_id = serializers.CharField(required=False, max_length=200)
    user_id = serializers.CharField(required=False, max_length=200)
    assignment_date = serializers.CharField(required=False, max_length=200)
    assignment_time = serializers.CharField(required=False, max_length=200)
    # completion_date = serializers.CharField(required=False, max_length=200)
    # completion_time = serializers.CharField(required=False, max_length=200)
    # remark = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ServiceAssignment
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_service_assignment_validated_data(validated_data)
        if ServiceAssignment.objects.filter(sa_id=validated_data['sa_id'], is_active=True).exists():
            raise CustomAPIException(SERVICE_ASSIGNMENT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            assignment_obj = super(ServiceAssignmentSerializer, self).create(validated_data)            
            assignment_obj.created_by = user.id
            assignment_obj.created_date = datetime.utcnow()
            assignment_obj.tenant = user.tenant
            assignment_obj.status_id = 1
            assignment_obj.is_active = True
            assignment_obj.save()
            
            return assignment_obj

    def update(self, instance, validated_data, user):
        validated_data = set_service_assignment_validated_data(validated_data)
        with transaction.atomic():
            assignment_obj = super(ServiceAssignmentSerializer, self).update(instance, validated_data)
            assignment_obj.updated_by = user.id
            assignment_obj.updated_date = datetime.utcnow()
            assignment_obj.is_active = False
            assignment_obj.save()
            return assignment_obj


class ServiceAssignmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    sa_id = ServiceAppointmentViewSerializer(many=False, required=True, source='get_service_appointment')
    user_id = GetUserSerializer(many=False, required=True, source='get_user')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = ServiceAssignment
        fields = ('__all__')