__author__ = "aki"

from django.urls import path
from v1.tenant.views.tenant_invoice import TenantInvoiceList, TenantInvoice, TenantInvoiceDetail
from v1.tenant.views.tenant_invoice_payment import TenantInvoicePaymentList, TenantInvoicePayment, \
    TenantInvoicePaymentDetail
from v1.tenant.views.tenant_subscription import TenantSubscriptionList, TenantSubscription, TenantSubscriptionDetail
from v1.tenant.views.tenant import TenantList,TenantDetail,Tenant
from v1.tenant.views.tenant_module import TenantModuleList, TenantModule, TenantModuleDetail
from v1.tenant.views.tenant_sub_module import TenantSubModuleList, TenantSubModuleDetail, TenantSubModule
from v1.tenant.views.tenant_subscription_plan import TenantSubscriptionPlanList
from v1.tenant.views.tenant_subscription_plan_rate import TenantSubscriptionPlanRateList
from v1.tenant.views.tenant_summary import TenantSummaryDetail
from v1.tenant.views.tenant_bank_detail import TenantBankDetail,TenantBank
from v1.tenant.views.tenant_bank_detail import TenantBankList
from v1.tenant.views.tenant_status import TenantStatusList


urlpatterns = [
    path('', Tenant.as_view(), name='tenant'),
    path('list', TenantList.as_view(), name='tenant_list'),
    path('<uuid:id_string>', TenantDetail.as_view(), name='tenant_details'),

    path('<uuid:id_string>/module/list', TenantModuleList.as_view(), name='tenant_module_list'),
    path('<uuid:id_string>/module', TenantModule.as_view(), name='tenant_module'),
    path('module/<uuid:id_string>', TenantModuleDetail.as_view(), name='tenant_module_details'),

    path('<uuid:id_string>/submodule/list', TenantSubModuleList.as_view(), name='tenant_submodule_list'),
    path('<uuid:id_string>/submodule', TenantSubModule.as_view(), name='tenant_submodule'),
    path('submodule/<uuid:id_string>', TenantSubModuleDetail.as_view(), name='tenant_submodule_details'),

    path('<uuid:id_string>/bank/list', TenantBankList.as_view(), name='tenant_bank_list'),
    path('<uuid:id_string>/bank', TenantBank.as_view(), name='tenant_bank'),
    path('bank/<uuid:id_string>', TenantBankDetail.as_view(), name='tenant_bank_details'),

    path('<uuid:id_string>/subscription/list', TenantSubscriptionList.as_view(), name='tenant_subscription_list'),
    path('<uuid:id_string>/subscription', TenantSubscription.as_view(), name='tenant_subscription'),
    path('subscription/<uuid:id_string>', TenantSubscriptionDetail.as_view(), name='tenant_subscription_details'),

    path('<uuid:id_string>/invoice/list', TenantInvoiceList.as_view(), name='tenant_invoice_list'),
    path('<uuid:id_string>/invoice', TenantInvoice.as_view(), name='tenant_invoice'),
    path('invoice/<uuid:id_string>', TenantInvoiceDetail.as_view(), name='tenant_invoice_details'),

    path('<uuid:id_string>/payment/list', TenantInvoicePaymentList.as_view(), name='tenant_invoice_payment_list'),
    path('<uuid:id_string>/payment', TenantInvoicePayment.as_view(), name='tenant_invoice_payment'),
    path('payment/<uuid:id_string>', TenantInvoicePaymentDetail.as_view(), name='tenant_invoice_payment_details'),

    path('subscription-plan/list', TenantSubscriptionPlanList.as_view(), name='tenant_subscription_plan_list'),
    path('subscription-plan-rate/list', TenantSubscriptionPlanRateList.as_view(),
         name='tenant_subscription_plan_rate_list'),
    path('status', TenantStatusList.as_view(), name='tenant_status_list'),
    path('<uuid:id_string>/summary', TenantSummaryDetail.as_view(), name='tenant_summary'),
]