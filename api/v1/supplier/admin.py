__author__ = "aki"

from django.contrib import admin
from v1.supplier.models.product_category import ProductCategory
from v1.supplier.models.product_subcategory import ProductSubCategory
from v1.supplier.models.supplier_invoice import SupplierInvoice
from v1.supplier.models.supplier_payment import SupplierPayment
from v1.supplier.models.supplier_product import SupplierProduct
from v1.supplier.models.supplier_service import SupplierService
from v1.supplier.models.supplier_status import SupplierStatus
from v1.supplier.models.supplier import Supplier

admin.site.register(SupplierStatus)
admin.site.register(Supplier)
admin.site.register(SupplierService)
admin.site.register(SupplierProduct)
admin.site.register(SupplierPayment)
admin.site.register(SupplierInvoice)
admin.site.register(ProductSubCategory)
admin.site.register(ProductCategory)
