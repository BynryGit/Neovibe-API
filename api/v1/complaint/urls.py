from django.urls import path
from v1.complaint.views.complaint import *

urlpatterns = [
    path('assignment/list', ComplaintAssignmentList.as_view()),
    path('<uuid:id_string>/', ComplaintDetail.as_view()),
    path('<uuid:id_string>/accept', ComplaintAccept.as_view()),
    path('<uuid:id_string>/reject', ComplaintReject.as_view()),
    path('<uuid:id_string>/complete', ComplaintComplete.as_view()),
]