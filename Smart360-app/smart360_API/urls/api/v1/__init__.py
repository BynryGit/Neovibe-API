__author__ = "aki"

from django.urls import path, include
from userapp.urls.api import v1 as userapi

urlpatterns = [
    path('user/', include(userapi)),
]