from django.urls import path

from v1.registration.views.common_functions import get_area_by_id_string

urlpatterns = [
    path('', get_area_by_id_string)
]