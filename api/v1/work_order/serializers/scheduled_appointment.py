__author__ = "Priyanka"

from django.db import transaction
from datetime import datetime
from rest_framework import serializers, status
import random
from rest_framework.validators import UniqueTogetherValidator
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.work_order.models.scheduled_appointment import ScheduledAppointment
from v1.work_order.views.common_functions import set_schedule_appointment_validated_data
from v1.tenant.serializers.tenant import TenantStatusViewSerializer
from v1.consumer.serializers.consumer_master import ConsumerListSerializer
from v1.asset.serializer.asset import AssetShortListSerializer
from v1.work_order.serializers.work_order_master import WorkOrderMasterShortListSerializer
from v1.work_order.views.common_functions import generate_service_appointment_no
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import SCHEDULE_APPOINTMENT_ALREADY_EXIST
from v1.userapp.serializers.user import GetUserSerializer


class ScheduledAppointmentSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    user_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ScheduledAppointment
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_schedule_appointment_validated_data(validated_data)
        if ScheduledAppointment.objects.filter(user_id=validated_data['user_id'],
                                             assignment_date=validated_data['assignment_date'], is_active=True).exists():
            raise CustomAPIException(SCHEDULE_APPOINTMENT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            appointment_obj = super(ScheduledAppointmentSerializer, self).create(validated_data)
            appointment_obj.created_by = user.id
            appointment_obj.created_date = datetime.utcnow()
            appointment_obj.tenant = user.tenant
            appointment_obj.save()
            return appointment_obj

    def update(self, instance, validated_data, user):
        validated_data = set_service_appointment_validated_data(validated_data)
        with transaction.atomic():
            appointment_obj = super(ScheduledAppointmentSerializer, self).update(instance, validated_data)
            appointment_obj.state = 5
            appointment_obj.updated_by = user.id
            appointment_obj.updated_date = datetime.utcnow()
            appointment_obj.is_active = True
            appointment_obj.save()
            return appointment_obj


class ScheduledAppointmentViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    user_id = GetUserSerializer(many=False, required=True, source='get_user')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = ScheduledAppointment
        fields = ('__all__')