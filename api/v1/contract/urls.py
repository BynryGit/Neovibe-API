__author__ = "aki"

from django.urls import path

from v1.contract.views.contract import Contract, ContractList, ContractDetail
from v1.contract.views.contract_demand import ContractDemandList, ContractDemand, ContractDemandDetail
from v1.contract.views.contract_invoice import ContractInvoiceList, ContractInvoice, ContractInvoiceDetail
from v1.contract.views.contract_payment import ContractPaymentList, ContractPayment, ContractPaymentDetail
from v1.contract.views.contract_period import ContractperiodList
from v1.contract.views.contract_status import ContractStatusList
from v1.contract.views.contract_type import ContractTypeList, ContractTypeDetail, ContractType
from v1.contract.views.term_and_condition import ContractTermAndConditionList, ContractTermAndCondition, \
    ContractTermAndConditionDetail
from v1.contract.views.contract_subtype import ContractSubTypeList, ContractSubTypeDetail, ContractSubType
from v1.contract.views.contract_period import ContractperiodList, ContractPeriodDetail, ContractPeriod


urlpatterns = [
    path('', Contract.as_view(), name='contract'),
    path('<uuid:id_string>/list', ContractList.as_view(), name='contract_list'),
    path('<uuid:id_string>', ContractDetail.as_view(),name='contract_detail'),

    path('<uuid:id_string>/invoice/list', ContractInvoiceList.as_view(),name='contract_invoice_list'),
    path('<uuid:id_string>/invoice', ContractInvoice.as_view(), name='contract_invoice'),
    path('invoice/<uuid:id_string>', ContractInvoiceDetail.as_view(),name='contract_invoice_detail'),

    path('<uuid:id_string>/payment/list', ContractPaymentList.as_view(),name='contract_payment_list'),
    path('<uuid:id_string>/payment', ContractPayment.as_view(), name='contract_payment'),
    path('payment/<uuid:id_string>', ContractPaymentDetail.as_view(),name='contract_payment_detail'),

    path('<uuid:id_string>/demand/list', ContractDemandList.as_view(),name='contract_demand_list'),
    path('<uuid:id_string>/demand', ContractDemand.as_view(), name='contract_demand'),
    path('demand/<uuid:id_string>', ContractDemandDetail.as_view(),name='contract_demand_detail'),

    path('<uuid:id_string>/terms-and-condition/list', ContractTermAndConditionList.as_view(),name='contract_term_and_condition_list'),
    path('<uuid:id_string>/terms-and-condition', ContractTermAndConditionDetail.as_view(), name='contract_term_and_condition_detail'),
    path('terms-and-condition', ContractTermAndCondition.as_view(),name='contract_term_and_condition'),

    path('status/list', ContractStatusList.as_view(), name='contract_status_list'),
    path('<uuid:id_string>/type/list', ContractTypeList.as_view(), name='contract_type_list'),
    path('<uuid:id_string>/type', ContractTypeDetail.as_view(), name='contract_type_detail'),
    path('type', ContractType.as_view(), name='contract_type'),
    path('<uuid:id_string>/period/list', ContractperiodList.as_view(), name='Contract_period_list'),

    path('<uuid:id_string>/subtype/list', ContractSubTypeList.as_view(), name='contract_subtype_list'),
    path('<uuid:id_string>/subtype', ContractSubTypeDetail.as_view(), name='contract_subtype_detail'),
    path('subtype', ContractSubType.as_view(), name='contract_subtype'),

    path('<uuid:id_string>/period/list', ContractperiodList.as_view(), name='contract_period_list'),
    path('<uuid:id_string>/period', ContractPeriodDetail.as_view(), name='contract_period_detail'),
    path('period', ContractPeriod.as_view(), name='contract_period'),

]