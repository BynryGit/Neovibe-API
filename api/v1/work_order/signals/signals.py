from django.db import transaction
from django.dispatch import receiver
from rest_framework import status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.signals.signals import consumer_service_request_created
from v1.work_order.serializers.service_appointment import ServiceAppointmentSerializer


# Signal receiver for consumer
@receiver([consumer_service_request_created, ])
def after_consumer_service_request_created(sender, **kwargs):
    try:
        service_appointment = super(ServiceAppointmentSerializer, ServiceAppointmentSerializer()).create(kwargs['data'])
    except Exception as e:
        raise CustomAPIException("Error in creating service appointment",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
