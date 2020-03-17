__author__ = "aki"

from django.urls import path

from masterapp.api.v1.user_lookup import PrivilegeApiView
from userapp.api.v1.user import LoginApiView

urlpatterns = [
    path('login', LoginApiView.as_view()),
    path('privilege', PrivilegeApiView.as_view()),
]