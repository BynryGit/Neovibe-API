from django.urls import path
from v1.userapp.views.role import RoleList, PrivilegeDetail

urlpatterns = [
    path('', RoleList.as_view()),
    path('list/', RoleList.as_view()),
    path('privileges/', PrivilegeDetail.as_view()),
]