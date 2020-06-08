__author__ = "aki"

from django.urls import path

from v1.tender.views.tender import Tender, TenderList, TenderDetail

urlpatterns = [
    path('', Tender.as_view(), name='tender'),
    path('list', TenderList.as_view(), name='tender_list'),
    path('<uuid:id_string>', TenderDetail.as_view(),name='tender_detail'),

    # path('<uuid:id_string>/quotation/list', TenderQuotationList.as_view(),name='tender_quotation_list'),
    # path('<uuid:id_string>/quotation', TenderQuotation.as_view(), name='tender_quotation'),
    # path('quotation/<uuid:id_string>', TenderQuotationDetail.as_view(),name='tender_quotation_detail'),
    #
    # path('<uuid:id_string>/vendor/list', TenderVendorList.as_view(),name='tender_vendor_list'),
    # path('<uuid:id_string>/vendor', TenderVendor.as_view(), name='tender_vendor'),
    # path('vendor/<uuid:id_string>', TenderVendorDetail.as_view(),name='tender_vendor_detail'),
    #
    # path('status/list', TenderStatusList.as_view(), name='Tender_status_list'),
]