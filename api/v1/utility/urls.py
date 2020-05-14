__author__ = "aki"

from django.urls import path

from v1.utility.views.document import Documents, DocumentDetails
from v1.utility.views.notes import Notes, NoteDetails
from v1.utility.views.numformat import Numformat
from v1.utility.views.utility import UtilityListDetail, UtilityDetail, Utility
from v1.utility.views.summary import UtilityUsageSummaryDetail
from v1.utility.views.utility_module import UtilityModules, UtilityModuleDetail
from v1.utility.views.utility_sub_module import UtilitySubModules

urlpatterns = [
    path('', Utility.as_view(), name='utility'),
    path('list', UtilityListDetail.as_view(), name='utility_list'),
    path('<uuid:id_string>', UtilityDetail.as_view(),name='utility_detail'),
    path('<uuid:id_string>/summary', UtilityUsageSummaryDetail.as_view(), name='utility_summary'),
    path('<uuid:id_string>/modules', UtilityModules.as_view(), name='utility_module_list'),
    path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),
    path('<uuid:id_string>/submodules', UtilitySubModules.as_view(), name='utility_submodule_list'),
    path('submodule/<uuid:id_string>', UtilitySubModules.as_view(), name='utility_submodule_details'),
    path('<uuid:id_string>/documents', Documents.as_view(), name='utility_document_list'),
    path('document/<uuid:id_string>', DocumentDetails.as_view(), name='utility_document_details'),
    path('<uuid:id_string>/notes', Notes.as_view(), name='utility_notes_list'),
    path('note/<uuid:id_string>', NoteDetails.as_view(), name='utility_note_details'),
    path('<uuid:id_string>/numformat', Numformat.as_view(),name='numformat'),
]