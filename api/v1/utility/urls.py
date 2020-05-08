__author__ = "aki"

from django.urls import path

from v1.utility.views.utility import UtilityListDetail, UtilityDetail

urlpatterns = [
    path('', UtilityListDetail.as_view(), name='utility_list'),
    path('<uuid:id_string>/', UtilityDetail.as_view(),name='utility_detail'),
]