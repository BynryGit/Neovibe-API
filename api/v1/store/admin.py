from django.contrib import admin
from v1.store.models.store_type import StoreType
from v1.store.models.store_location import StoreLocation
from v1.store.models.receipt import Receipt
from v1.store.models.store_master import StoreMaster


admin.site.register(StoreMaster)
admin.site.register(StoreType)
admin.site.register(StoreLocation)
admin.site.register(Receipt)



