__author__ = "Gauri"

from django.urls import path
from v1.tenant.views.tenant import TenantList,TenantDetail,Tenant


urlpatterns = [
    path('list', TenantList.as_view()),
    path('', Tenant.as_view()),
    path('<uuid:id_string>', TenantDetail.as_view()),


    # path('<uuid:id_string>/', TenantDetail.as_view(),name='tenant_detail'),

    # path('<uuid:id_string>/summary', UtilityUsageSummaryDetail.as_view(), name='utility_summary'),
    # path('<uuid:id_string>/modules', UtilityModules.as_view(), name='utility_module_list'),
    # path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),
    # path('<uuid:id_string>/submodules', UtilitySubModules.as_view(), name='utility_submodule_list'),
    # path('submodule/<uuid:id_string>', UtilitySubModules.as_view(), name='utility_submodule_details'),
    # path('<uuid:id_string>/documents', Documents.as_view(), name='utility_document_list'),
    # path('document/<uuid:id_string>', DocumentDetails.as_view(), name='utility_document_details'),
    # path('<uuid:id_string>/notes', Notes.as_view(), name='utility_notes_list'),
    # path('note/<uuid:id_string>', NoteDetails.as_view(), name='utility_note_details'),
]