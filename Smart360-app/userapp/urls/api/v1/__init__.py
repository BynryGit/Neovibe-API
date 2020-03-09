__author__ = "aki"

from django.urls import path
from userapp.api.v1.user import LoginApiView

urlpatterns = [
    path('login', LoginApiView.as_view()),
]