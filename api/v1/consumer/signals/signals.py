from django.dispatch import receiver, Signal
from rest_framework import status
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_master import get_consumer_by_registration_id
from v1.consumer.views.common_functions import create_consumer_after_registration
from v1.registration.signals.signals import registration_approved

# Signals for work order service appointment
consumer_service_request_created = Signal()


# Signal receiver for consumer
@receiver([registration_approved])
def after_registration_approved(sender, **kwargs):
    try:
        consumer = get_consumer_by_registration_id(sender.id)
        consumer.is_active = True
        consumer.save()
    except Exception as e:
        raise CustomAPIException(str(e), status_code=status.HTTP_412_PRECONDITION_FAILED)


# Signal receiver for consumer
@receiver([consumer_service_request_created, ])
def after_consumer_service_request_created(sender, **kwargs):
    try:
        service_appointment = super(ServiceAppointmentSerializer, ServiceAppointmentSerializer()).create(kwargs['data'])
    except Exception as e:
        raise CustomAPIException("Error in creating service appointment",
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
