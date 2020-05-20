from django.urls import path

from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.views.role import RoleList, Role, RoleDetail

urlpatterns = [

    path('', Role.as_view()),
    path('<uuid:id_string>', RoleDetail.as_view()),
    path('list/', RoleList.as_view()),

    path('privileges/', RolePrivilege.as_view()),

]