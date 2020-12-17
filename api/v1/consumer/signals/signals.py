from django.dispatch import receiver
from rest_framework import status
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.registration.signals.signals import registration_approved


# Signal receiver for consumer
@receiver([registration_approved])
def after_registration_approved(sender, **kwargs):
    try:
        create_consumer_after_registration(sender.id)
    except Exception as e:
        raise CustomAPIException(str(e),status_code=status.HTTP_412_PRECONDITION_FAILED)
