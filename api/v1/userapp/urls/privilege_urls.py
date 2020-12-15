from django.urls import path

from v1.userapp.views.privilege import PrivilegeList, Privilege, PrivilegeDetail

urlpatterns = [

    path('', Privilege.as_view()),
    path('<uuid:id_string>', PrivilegeDetail.as_view()),
    path('list/', PrivilegeList.as_view()),

]