__author__ = "aki"

from django.urls import path, include
from django.contrib import admin
from smart360_API.urls import api

urlpatterns = [
    path('api/', include(api)),
    path('admin/', admin.site.urls),
]