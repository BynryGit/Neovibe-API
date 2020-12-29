from rest_framework import serializers
from v1.work_order.models.service_appointment_status import ServiceAppointmentStatus



class ServiceAppointmentStatusListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceAppointmentStatus
        fields = ('status','id_string')


