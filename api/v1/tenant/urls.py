__author__ = "Gauri"

from django.urls import path
from v1.tenant.views.invoice import TenantInvoiceList, TenantInvoice, TenantInvoiceDetail
from v1.tenant.views.payment import TenantInvoicePaymentList, TenantInvoicePayment, TenantInvoicePaymentDetail
from v1.tenant.views.subscription import SubscriptionList, Subscription, SubscriptionDetail
from v1.tenant.views.subscription_plan import SubscriptionPlanList, SubscriptionPlan, SubscriptionPlanDetail
from v1.tenant.views.subscription_rate import SubscriptionPlanRate
from v1.tenant.views.tenant import TenantList,TenantDetail,Tenant
from v1.tenant.views.tenant_sub_module import TenantSubModuleList, TenantSubModuleDetail, TenantSubmodule
from v1.tenant.views.document import TenantDocumentList, TenantDocumentDetail
from v1.tenant.views.notes import TenantNoteDetail, TenantNoteList
from v1.tenant.views.summary import TenantSummaryDetail
from v1.tenant.views.bank_detail import TenantBankDetail,TenantBank
from v1.tenant.views.bank_detail import BankList

urlpatterns = [
    path('', Tenant.as_view(), name='tenant'),
    path('list', TenantList.as_view(), name='tenant_list'),
    path('<uuid:id_string>', TenantDetail.as_view(), name='tenant_detail'),

    path('submodule/list', TenantSubModuleList.as_view(), name='tenant_submodule_list'),
    path('submodule/<uuid:id_string>', TenantSubModuleDetail.as_view(), name='tenant_submodule_details'),
    path('submodule', TenantSubmodule.as_view(), name='tenant_submodule'),

    path('<uuid:id_string>/documents', TenantDocumentList.as_view(), name='tenant_document_list'),
    path('document/<uuid:id_string>', TenantDocumentDetail.as_view(), name='tenant_document_details'),

    path('<uuid:id_string>/notes', TenantNoteList.as_view(), name='tenant_notes_list'),
    path('note/<uuid:id_string>', TenantNoteDetail.as_view(), name='tenant_note_details'),

    path('<uuid:id_string>/summary', TenantSummaryDetail.as_view(), name='tenant_summary'),

    path('bank/list', BankList.as_view()),
    path('bank/', TenantBank.as_view()),
    path('bank/<uuid:id_string>', TenantBankDetail.as_view()),

    path('subscription/list', SubscriptionList.as_view()),
    path('subscription/', Subscription.as_view()),
    path('subscription/<uuid:id_string>', SubscriptionDetail.as_view()),

    path('subscription-plan/list', SubscriptionPlanList.as_view()),
    path('subscription-plan/', SubscriptionPlan.as_view()),
    path('subscription-plan/<uuid:id_string>', SubscriptionPlanDetail.as_view()),

    path('subscription-rate/list', SubscriptionList.as_view()),
    path('subscription-rate/', SubscriptionPlanRate.as_view()),
    path('subscription-rate/<uuid:id_string>', SubscriptionDetail.as_view()),

    path('invoice/list', TenantInvoiceList.as_view()),
    path('invoice/', TenantInvoice.as_view()),
    path('invoice/<uuid:id_string>', TenantInvoiceDetail.as_view()),

    path('payment/list', TenantInvoicePaymentList.as_view()),
    path('payment/', TenantInvoicePayment.as_view()),
    path('payment/<uuid:id_string>', TenantInvoicePaymentDetail.as_view()),
    # path('payment/<uuid:id_string>', PaymentDetail.as_view()),
    # path('bank-detail/', GetBankList.as_view()),
    # path('<uuid:id_string>/summary', UtilityUsageSummaryDetail.as_view(), name='utility_summary'),
    # path('<uuid:id_string>/modules', UtilityModules.as_view(), name='utility_module_list'),
    # path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),
]