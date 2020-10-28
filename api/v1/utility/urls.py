__author__ = "aki"

from django.urls import path
from v1.utility.views.document import UtilityDocumentList, UtilityDocumentDetail
from v1.utility.views.document_sub_type import UtilityDocumentSubTypeList
from v1.utility.views.document_type import UtilityDocumentTypeList
from v1.utility.views.notes import UtilityNoteList, UtilityNoteDetail
from v1.utility.views.numformat import UtilityNumformatDetail
from v1.utility.views.status import UtilityStatusList
from v1.utility.views.utility import UtilityList, UtilityDetail, Utility
from v1.utility.views.summary import UtilitySummaryDetail
from v1.utility.views.utility_module import UtilityModuleList, UtilityModuleDetail
from v1.utility.views.utility_sub_module import UtilitySubModuleList, UtilitySubModuleDetail, \
    UtilitySubModuleListByModule
from v1.userapp.views.role_type import RoleTypeList
from v1.userapp.views.role_sub_type import RoleSubTypeByRoleType


urlpatterns = [
    path('', Utility.as_view(), name='utility'),
    path('list', UtilityList.as_view(), name='utility_list'),
    path('<uuid:id_string>', UtilityDetail.as_view(),name='utility_detail'),

    path('<uuid:id_string>/summary', UtilitySummaryDetail.as_view(), name='utility_summary'),

    path('<uuid:id_string>/module/list', UtilityModuleList.as_view(), name='utility_module_list'),
    path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),

    path('<uuid:id_string>/submodule/list', UtilitySubModuleList.as_view(), name='utility_submodule_list'),
    path('submodule/<uuid:id_string>', UtilitySubModuleDetail.as_view(), name='utility_submodule_details'),
    path('module/<uuid:id_string>/submodule/list', UtilitySubModuleListByModule.as_view(),
         name='utility_submodule_list_by_module'),

    path('<uuid:id_string>/documents', UtilityDocumentList.as_view(), name='utility_document_list'),
    path('document/<uuid:id_string>', UtilityDocumentDetail.as_view(), name='utility_document_details'),

    path('<uuid:id_string>/notes', UtilityNoteList.as_view(), name='utility_notes_list'),
    path('note/<uuid:id_string>', UtilityNoteDetail.as_view(), name='utility_note_details'),

    path('<uuid:id_string>/numformat', UtilityNumformatDetail.as_view(),name='numformat'),

    path('<uuid:id_string>/status/list', UtilityStatusList.as_view(),name='utility_status_list'),
    path('<uuid:id_string>/document-type/list', UtilityDocumentTypeList.as_view(), name='utility_document_type_list'),
    path('<uuid:id_string>/document-sub-type/list', UtilityDocumentSubTypeList.as_view(), name='utility_document_sub_type_list'),

    path('<uuid:id_string>/role-type/list', RoleTypeList.as_view()),
    path('role-type/<uuid:id_string>/role-subtype/list', RoleSubTypeByRoleType.as_view(),name='utility_status_list'),
]
