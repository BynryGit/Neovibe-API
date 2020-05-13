from django.urls import path
from v1.userapp.views.role import RoleList, PrivilegeDetail, Roles
from v1.userapp.views.user import Users, UserList, Bank

urlpatterns = [
    path('<uuid:id_string>', Roles.as_view()),
    path('list/', RoleList.as_view()),
    path('privileges/', PrivilegeDetail.as_view()),
    path('<uuid:id_string>', Users.as_view()),
    path('list/', UserList.as_view()),
    path('bank/', Bank.as_view()),
]