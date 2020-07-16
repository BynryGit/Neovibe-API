__author__ = "Rohan"


import logging
from django.dispatch import receiver, Signal
from rest_framework import status
from v1.commonapp.models.state_configuration import StateConfiguration, STATE_CONFIGURATION_DICT
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.payment.models.consumer_payment import PAYMENT_DICT
from v1.registration.models import registrations


# Local logging
logger = logging.getLogger('django')


# Default switch cases
def payment_switch(payment_state, registration):
    try:
        if payment_state == PAYMENT_DICT["CREATED"]:
            registration.change_state(registrations.REGISTRATION_DICT["PENDING"])
        if payment_state == PAYMENT_DICT["APPROVED"]:
            registration.change_state(registrations.REGISTRATION_DICT["APPROVED"])
        if payment_state == PAYMENT_DICT["REJECTED"]:
            registration.change_state(registrations.REGISTRATION_DICT["PENDING"])
    except Exception as e:
        raise CustomAPIException(str(e),status_code=status.HTTP_412_PRECONDITION_FAILED)


# Signals for registration from payments
registration_payment_created = Signal()
registration_payment_approved = Signal()


# Signals for consumer from registration
registration_approved = Signal()


# Signal receiver for registration
@receiver([registration_payment_created, registration_payment_approved])
def after_payment(sender, **kwargs):
    try:
        registration = registrations.get_registration_by_id(sender.identification_id)
        if StateConfiguration.objects.filter(utility = registration.utility, sender_object = STATE_CONFIGURATION_DICT['PAYMENT'], sender_state = sender.state,
                                             receiver_object = STATE_CONFIGURATION_DICT['REGISTRATION'], is_active = True).exists():
            state_object = StateConfiguration.objects.get(utility = registration.utility, sender_state = sender.state,
                                             sender_object = STATE_CONFIGURATION_DICT['PAYMENT'], receiver_object = STATE_CONFIGURATION_DICT['REGISTRATION'])
            registration.change_state(state_object.receiver_state)
        else:
            payment_switch(sender.state, registration)
    except Exception as e:
        raise CustomAPIException(str(e),status_code=status.HTTP_412_PRECONDITION_FAILED)





