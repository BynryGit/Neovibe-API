from django.contrib import admin
from v1.billing.models.bill_status import BillStatus
from v1.billing.models.consumer_outstanding import ConsumerOutstanding
from v1.billing.models.invoice_bill import InvoiceBill
from v1.billing.models.route_detail import RouteDetail
from v1.billing.models.unit_range import UnitRange

admin.site.register(InvoiceBill)
admin.site.register(ConsumerOutstanding)
admin.site.register(BillStatus)
admin.site.register(UnitRange)
admin.site.register(RouteDetail)