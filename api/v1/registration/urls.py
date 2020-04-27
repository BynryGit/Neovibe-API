from django.urls import path

from v1.registration.views import view

urlpatterns = [
    path('', view)
]