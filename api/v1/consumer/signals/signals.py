from django.dispatch import receiver
from v1.registration.signals.signals import registration_completed








# Signal receiver for consumer
@receiver([registration_completed])
def after_registration_completed(sender, **kwargs):
    try:
        pass
    except Exception as e:
        pass