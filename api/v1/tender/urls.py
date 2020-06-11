__author__ = "aki"

from django.urls import path
from v1.tender.views.tender import Tender, TenderList, TenderDetail
from v1.tender.views.tender_quotation import TenderQuotationList, TenderQuotation, TenderQuotationDetail
from v1.tender.views.tender_status import TenderStatusList
from v1.tender.views.tender_terms_and_conditions import TenderTermAndConditionList, TenderTermAndCondition, \
    TenderTermAndConditionDetail
from v1.tender.views.tender_type import TenderTypeList
from v1.tender.views.tender_vendor import TenderVendorList, TenderVendor, TenderVendorDetail

urlpatterns = [
    path('', Tender.as_view(), name='tender'),
    path('list', TenderList.as_view(), name='tender_list'),
    path('<uuid:id_string>', TenderDetail.as_view(),name='tender_detail'),

    path('<uuid:id_string>/quotation/list', TenderQuotationList.as_view(),name='tender_quotation_list'),
    path('<uuid:id_string>/quotation', TenderQuotation.as_view(), name='tender_quotation'),
    path('quotation/<uuid:id_string>', TenderQuotationDetail.as_view(),name='tender_quotation_detail'),

    path('<uuid:id_string>/vendor/list', TenderVendorList.as_view(),name='tender_vendor_list'),
    path('<uuid:id_string>/vendor', TenderVendor.as_view(), name='tender_vendor'),
    path('vendor/<uuid:id_string>', TenderVendorDetail.as_view(),name='tender_vendor_detail'),

    path('<uuid:id_string>/t&c/list', TenderTermAndConditionList.as_view(),name='tender_term_and_condition_list'),
    path('<uuid:id_string>/t&c', TenderTermAndCondition.as_view(), name='tender_term_and_condition'),
    path('t&c/<uuid:id_string>', TenderTermAndConditionDetail.as_view(),name='tender_term_and_condition_detail'),

    path('status/list', TenderStatusList.as_view(), name='tender_status_list'),
    path('type/list', TenderTypeList.as_view(), name='tender_type_list'),
]