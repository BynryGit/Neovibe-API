from django.urls import path
from v1.complaint.views.complaint import *
from v1.complaint.views.complaint_type import ComplaintTypeList,ComplaintTypeDetail,ComplaintType
from v1.complaint.views.complaint_subtype import ComplaintSubType,ComplaintSubTypeDetail,ComplaintSubTypeList

urlpatterns = [
    path('assignment/list', ComplaintAssignmentList.as_view()),
    path('<uuid:id_string>/', ComplaintDetail.as_view()),
    path('<uuid:id_string>/accept', ComplaintAccept.as_view()),
    path('<uuid:id_string>/reject', ComplaintReject.as_view()),
    path('<uuid:id_string>/complete', ComplaintComplete.as_view()),
    path('utility/<uuid:id_string>/type/list', ComplaintTypeList.as_view()),
    path('type/<uuid:id_string>', ComplaintTypeDetail.as_view()),
    path('type', ComplaintType.as_view()),
    path('utility/<uuid:id_string>/subtype/list', ComplaintSubTypeList.as_view()),
    path('subtype/<uuid:id_string>', ComplaintSubTypeDetail.as_view()),
    path('subtype', ComplaintSubType.as_view()),
    path('utility/<uuid:id_string>/list', ComplaintList.as_view()),
]