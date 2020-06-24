import django.dispatch

payment_created = django.dispatch.Signal()

payment_approved = django.dispatch.Signal()