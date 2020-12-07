from django.urls import path

from v1.userapp.views.role import RoleList, Role, RoleDetail, GetRoleDetail
from v1.userapp.views.role_privilege import RolePrivilegeDetail
from v1.userapp.views.user_role import UserRoleByUtilityModules,UserRoleByUtilitySubModule

urlpatterns = [

    path('', Role.as_view()),
    path('<uuid:id_string>', RoleDetail.as_view()),
    path('list/', RoleList.as_view()),
    path('<uuid:id_string>/privileges/', RolePrivilegeDetail.as_view()),

    path('type/<uuid:type_id_string>/sub-type/<uuid:sub_type_id_string>', GetRoleDetail.as_view()),
    path('<uuid:user_id_string>/utility/<uuid:utility_id_string>', UserRoleByUtilityModules.as_view()),
    path('<uuid:user_id_string>/module/<uuid:module_id_string>', UserRoleByUtilitySubModule.as_view()),



]