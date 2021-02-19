from django.urls import path
from v1.userapp.views.document import UserDocument
from v1.userapp.views.login import LoginApiView, LogoutApiView
from v1.userapp.views.notes import UserNote
from v1.userapp.views.user import User, UserList, UserDetail, ResourceList,BulkAssignResourceList,UserNoteList,UserNote, UserLifeCycleList
from v1.userapp.views.user_area import UserArea
from v1.userapp.views.user_bank import UserBankDetail
from v1.userapp.views.user_privilege import UserPrivilegeDetail
from v1.userapp.views.user_role import UserRole
from v1.userapp.views.user_skill import UserSkill
from v1.userapp.views.user_utility import UserUtility,UesrUtilityList
from v1.userapp.views.user_sub_type import UserSubTypeByUserType
from v1.userapp.views.user_role import UserRoleByUtilityModules,UserRoleByUtilitySubModule,ModulePrivilegesList
from v1.userapp.views.field_agent_live_location import FieldAgentLiveLocationList

urlpatterns = [
    path('', User.as_view(), name='create-user'),
    path('<uuid:id_string>', UserDetail.as_view()),
    path('list/', UserList.as_view()),
    path('<uuid:id_string>/bank/', UserBankDetail.as_view()),  
     
    path('type/<uuid:id_string>/sub-type/list', UserSubTypeByUserType.as_view()),

    path('<uuid:id_string>/role/', UserRole.as_view()),

    path('<uuid:id_string>/privilege/', UserPrivilegeDetail.as_view()),

    path('<uuid:id_string>/note/', UserNote.as_view()),

    path('<uuid:id_string>/document/', UserDocument.as_view()),

    path('<uuid:id_string>/utility/', UserUtility.as_view()),

    path('<uuid:id_string>/area/', UserArea.as_view()),

    path('tenant/<uuid:id_string>/utility/list', UesrUtilityList.as_view()),

    path('<uuid:id_string>/skill/', UserSkill.as_view()),

    path('login/', LoginApiView.as_view(), name='log-in'),

    path('logout/', LogoutApiView.as_view()),

    path('<uuid:user_id_string>/utility/<uuid:utility_id_string>', UserRoleByUtilityModules.as_view()),
    path('<uuid:user_id_string>/module/<uuid:module_id_string>', UserRoleByUtilitySubModule.as_view()),
    path('role/<uuid:role_id_string>/module/<uuid:module_id_string>/sub-module/<uuid:sub_module_id_string>',ModulePrivilegesList.as_view()),
    path('utility/<uuid:utility_id_string>/appointment/<uuid:appointment_id_string>/resource/list',ResourceList.as_view(),name="fitered_resource_list"),
    path('utility/<uuid:utility_id_string>/bulk-assign/resource/list',BulkAssignResourceList.as_view(),name="bulk_assign_resource_list"),
    path('<uuid:user_id_string>/utility/<uuid:utility_id_string>/note', UserNote.as_view(), name="add_user_notes_list"),
    path('<uuid:id_string>/note/list', UserNoteList.as_view(), name="user_notes_list"),
    path('<uuid:id_string>/life-cycle',UserLifeCycleList.as_view(),name="user_life_cycle")
]