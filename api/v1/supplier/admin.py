from django.contrib import admin
from v1.supplier.models.supplier_status import SupplierStatus
from v1.supplier.models.supplier_master import SupplierMaster

admin.site.register(SupplierStatus)
admin.site.register(SupplierMaster)
