__author__ = "aki"

from django.urls import path

from v1.utility.views.document import UtilityDocumentList, UtilityDocumentDetail
from v1.utility.views.notes import UtilityNoteList, UtilityNoteDetail
from v1.utility.views.numformat import UtilityNumformatDetail
from v1.utility.views.status import UtilityStatusList
from v1.utility.views.utility import UtilityList, UtilityDetail, Utility
from v1.utility.views.summary import UtilitySummaryDetail
from v1.utility.views.utility_module import UtilityModuleList, UtilityModuleDetail
from v1.utility.views.utility_sub_module import UtilitySubModuleList, UtilitySubModuleDetail

urlpatterns = [
    path('', Utility.as_view(), name='utility'),
    path('list', UtilityList.as_view(), name='utility_list'),
    path('<uuid:id_string>', UtilityDetail.as_view(),name='utility_detail'),
    path('<uuid:id_string>/summary', UtilitySummaryDetail.as_view(), name='utility_summary'),
    path('<uuid:id_string>/module/list', UtilityModuleList.as_view(), name='utility_module_list'),
    path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),
    path('<uuid:id_string>/submodule/list', UtilitySubModuleList.as_view(), name='utility_submodule_list'),
    path('submodule/<uuid:id_string>', UtilitySubModuleDetail.as_view(), name='utility_submodule_details'),
    path('<uuid:id_string>/documents', UtilityDocumentList.as_view(), name='utility_document_list'),
    path('document/<uuid:id_string>', UtilityDocumentDetail.as_view(), name='utility_document_details'),
    path('<uuid:id_string>/notes', UtilityNoteList.as_view(), name='utility_notes_list'),
    path('note/<uuid:id_string>', UtilityNoteDetail.as_view(), name='utility_note_details'),
    path('<uuid:id_string>/numformat', UtilityNumformatDetail.as_view(),name='numformat'),
    path('<uuid:id_string>/status/list', UtilityStatusList.as_view(),name='utility_status_list'),
]