__author__ = "aki"

from django.urls import path, include
from smart360_API.urls.api import v1 as v1_urls


urlpatterns = [
    path('v1/', include(v1_urls))
]