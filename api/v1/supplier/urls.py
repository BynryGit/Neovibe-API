__author__ = "aki"

from django.urls import path
from v1.supplier.views.supplier import SupplierList, SupplierDetail, Supplier
from v1.supplier.views.supplier_contract import SupplierContractList, SupplierContract, SupplierContractDetail
from v1.supplier.views.supplier_invoice import SupplierInvoiceList, SupplierInvoice, SupplierInvoiceDetail
from v1.supplier.views.supplier_payment import SupplierPaymentList, SupplierPayment, SupplierPaymentDetail
from v1.supplier.views.supplier_product import SupplierProductList, SupplierProduct, SupplierProductDetail
from v1.supplier.views.supplier_service import SupplierServiceList, SupplierService, SupplierServiceDetail
from v1.supplier.views.supplier_status import SupplierStatusList

urlpatterns = [
    path('', Supplier.as_view(), name='supplier'),
    path('<uuid:id_string>/list', SupplierList.as_view(), name='supplier_list'),
    path('<uuid:id_string>', SupplierDetail.as_view(),name='supplier_detail'),

    path('<uuid:id_string>/invoice/list', SupplierInvoiceList.as_view(),name='supplier_invoice_list'),
    path('<uuid:id_string>/invoice', SupplierInvoice.as_view(), name='supplier_invoice'),
    path('invoice/<uuid:id_string>', SupplierInvoiceDetail.as_view(),name='supplier_invoice_detail'),

    path('<uuid:id_string>/payment/list', SupplierPaymentList.as_view(),name='supplier_payment_list'),
    path('<uuid:id_string>/payment', SupplierPayment.as_view(), name='supplier_payment'),
    path('payment/<uuid:id_string>', SupplierPaymentDetail.as_view(),name='supplier_payment_detail'),

    path('<uuid:id_string>/product/list', SupplierProductList.as_view(),name='supplier_product_list'),
    path('<uuid:id_string>/product', SupplierProduct.as_view(), name='supplier_product'),
    path('product/<uuid:id_string>', SupplierProductDetail.as_view(),name='supplier_product_detail'),

    path('<uuid:id_string>/service/list', SupplierServiceList.as_view(),name='supplier_service_list'),
    path('<uuid:id_string>/service', SupplierService.as_view(), name='supplier_service'),
    path('service/<uuid:id_string>', SupplierServiceDetail.as_view(),name='supplier_service_detail'),

    path('<uuid:id_string>/contract/list', SupplierContractList.as_view(),name='supplier_contract_list'),
    path('<uuid:id_string>/contract', SupplierContract.as_view(), name='supplier_contract'),
    path('contract/<uuid:id_string>', SupplierContractDetail.as_view(),name='supplier_contract_detail'),

    path('status/list', SupplierStatusList.as_view(), name='supplier_status_list'),
]