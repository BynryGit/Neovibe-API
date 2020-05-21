__author__ = "aki"

from django.urls import path
from v1.supplier.views.supplier import SupplierList, SupplierDetail, Supplier
from v1.supplier.views.supplier_invoice import SupplierInvoiceList, SupplierInvoice, SupplierInvoiceDetail

urlpatterns = [
    path('', Supplier.as_view(), name='supplier'),
    path('list', SupplierList.as_view(), name='supplier_list'),
    path('<uuid:id_string>', SupplierDetail.as_view(),name='utility_detail'),
    path('<uuid:id_string>/invoice/list', SupplierInvoiceList.as_view(),name='supplier_invoice_list'),
    path('<uuid:id_string>/invoice', SupplierInvoice.as_view(), name='supplier_invoice'),
    path('invoice/<uuid:id_string>', SupplierInvoiceDetail.as_view(),name='supplier_invoice_detail'),
]