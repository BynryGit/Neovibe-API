__author__ = "Rohan"


import logging
import django.dispatch
from django.dispatch import receiver
from rest_framework import status
from api.constants import *
from v1.commonapp.models.state_configuration import StateConfiguration
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.registration.models.registrations import get_registration_by_id

# Local logging
logger = logging.getLogger('django')

# Just for reference
REGISTRATION_STATES = (
        (1, 'CREATED'),
        (2, 'PENDING'),
        (3, 'APPROVED'),
        (4, 'REJECTED'),
        (5, 'HOLD'),
        (6, 'COMPLETED'),
        (7, 'ARCHIVED'),
    )

# Just for reference
PAYMENT_STATES = (
        (1, 'CREATED'),
        (2, 'APPROVED'),
        (3, 'REJECTED'),
    )

# Default switch cases
def payment_switch(payment_state, registration):
    try:
        if payment_state == PAYMENT_DICT["CREATED"]:
            registration.change_state(REGISTRATION_DICT["PENDING"])
        if payment_state == PAYMENT_DICT["APPROVED"]:
            registration.change_state(REGISTRATION_DICT["PENDING"])
        if payment_state == PAYMENT_DICT["REJECTED"]:
            registration.change_state(REGISTRATION_DICT["PENDING"])
    except Exception as e:
        raise CustomAPIException(str(e),status_code=status.HTTP_412_PRECONDITION_FAILED)

# Signals for registration from payments
registration_payment_created = django.dispatch.Signal()
registration_payment_approved = django.dispatch.Signal()

# Signal receiver for registration
@receiver([registration_payment_created, registration_payment_approved])
def after_payment(sender, **kwargs):
    try:
        registration = get_registration_by_id(sender.identification_id)
        if StateConfiguration.objects.filter(utility = registration.utility, sender_object = 'Payment', receiver_object = 'Registration', is_active = True).exists():
            state_object = StateConfiguration.objects.get(utility = registration.utility, sender_object = 'Payment', receiver_object = 'Registration')
            if sender.state == state_object.sender_state:
                registration.change_state(state_object.receiver_state)
        else:
            payment_switch(sender.state, registration)
    except Exception as e:
        raise CustomAPIException(str(e),status_code=status.HTTP_412_PRECONDITION_FAILED)