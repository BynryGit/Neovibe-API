from django.urls import path
from v1.userapp.views.role import RoleList, PrivilegeDetail, Roles
from v1.userapp.views.user import Users, UserList

urlpatterns = [
    path('', Roles.as_view()),
    path('list/', RoleList.as_view()),
    path('privileges/', PrivilegeDetail.as_view()),
    path('', Users.as_view()),
    path('list/', UserList.as_view()),
]