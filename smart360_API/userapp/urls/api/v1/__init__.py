__author__ = "aki"

from django.urls import path
from userapp.api.v1.login import LoginApiView
from masterapp.api.v1.privilege import PrivilegeApiView

urlpatterns = [
    path('login', LoginApiView.as_view()),
    path('privilege', PrivilegeApiView.as_view()),
]