__author__ = "Gauri"

from django.urls import path

from v1.commonapp.models.notes import Notes
from v1.tenant.views.tenant import TenantList,TenantDetail,Tenant
from v1.tenant.views.tenant_sub_module import TenantSubModuleList, TenantSubModuleDetail
from v1.tenant.views.document import TenantDocumentList, TenantDocumentDetail
from v1.tenant.views.notes import TenantNoteDetail, TenantNoteList
from v1.tenant.views.summary import TenantSummaryDetail
from v1.tenant.views.bank_detail import BankList
# from v1.tenant.views.bank_detail import BankList,BankDetails


urlpatterns = [
    path('list', TenantList.as_view()),
    path('', Tenant.as_view()),
    path('<uuid:id_string>', TenantDetail.as_view()),

    path('<uuid:id_string>/submodule/list', TenantSubModuleList.as_view(), name='tenant_submodule_list'),
    path('submodule/<uuid:id_string>', TenantSubModuleDetail.as_view(), name='tenant_submodule_details'),

    path('<uuid:id_string>/documents', TenantDocumentList.as_view(), name='tenant_document_list'),
    path('document/<uuid:id_string>', TenantDocumentDetail.as_view(), name='tenant_document_details'),

    path('<uuid:id_string>/notes', TenantNoteList.as_view(), name='tenant_notes_list'),
    path('note/<uuid:id_string>', TenantNoteDetail.as_view(), name='tenant_note_details'),

    path('<uuid:id_string>/summary', TenantSummaryDetail.as_view(), name='tenant_summary'),

    path('bank/list', BankList.as_view()),
    # path('bank-detail/', GetBankList.as_view()),
    # path('bank/<uuid:id_string>', Bank.as_view()),



    # path('<uuid:id_string>/summary', UtilityUsageSummaryDetail.as_view(), name='utility_summary'),
    # path('<uuid:id_string>/modules', UtilityModules.as_view(), name='utility_module_list'),
    # path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),


]