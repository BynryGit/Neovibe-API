__author__ = "aki"

from django.urls import path
from v1.supplier.views.supplier import SupplierList, SupplierDetail, Supplier
from v1.supplier.views.supplier_contract import SupplierContractList, SupplierContract, SupplierContractDetail
from v1.supplier.views.supplier_invoice import SupplierInvoiceList, SupplierInvoice, SupplierInvoiceDetail
from v1.supplier.views.supplier_payment import SupplierPaymentList, SupplierPayment, SupplierPaymentDetail
from v1.supplier.views.supplier_product import SupplierProductList, SupplierProduct, SupplierProductDetail
from v1.supplier.views.supplier_service import SupplierServiceList, SupplierService, SupplierServiceDetail
from v1.supplier.views.supplier_status import SupplierStatusList
from v1.supplier.views.supplier_type import SupplierTypeList, SupplierTypeDetail, SupplierType
from v1.supplier.views.supplier_subtype import SupplierSubTypeList, SupplierSubTypeDetail, SupplierSubType
from v1.supplier.views.product_category import ProductCategoryList, ProductCategoryDetail, ProductCategory
from v1.supplier.views.product_subcategory import ProductSubCategoryList, ProductSubCategoryDetail, ProductSubCategory

urlpatterns = [
    path('', Supplier.as_view(), name='supplier'),
    path('list', SupplierList.as_view(), name='supplier_list'),
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

    path('<uuid:id_string>/type/list', SupplierTypeList.as_view(), name='supplier_type_list'),
    path('<uuid:id_string>/type', SupplierTypeDetail.as_view(), name='supplier_type_detail'),
    path('type', SupplierType.as_view(), name='supplier_type'),

    path('<uuid:id_string>/subtype/list', SupplierSubTypeList.as_view(), name='supplier_subtype_list'),
    path('<uuid:id_string>/subtype', SupplierSubTypeDetail.as_view(), name='supplier_subtype_detail'),
    path('subtype', SupplierSubType.as_view(), name='supplier_subtype'),

    path('<uuid:id_string>/product-category/list', ProductCategoryList.as_view(), name='product_category_list'),
    path('<uuid:id_string>/product-category', ProductCategoryDetail.as_view(), name='product_category_detail'),
    path('product-category', ProductCategory.as_view(), name='product_category'),

    path('<uuid:id_string>/product-subcategory/list', ProductSubCategoryList.as_view(), name='product_subcategory_list'),
    path('<uuid:id_string>/product-subcategory', ProductSubCategoryDetail.as_view(), name='product_subcategory_detail'),
    path('product-subcategory', ProductSubCategory.as_view(), name='product_subcategory'),


]