from django.contrib import admin
from v1.billing.models.bill_month import BillMonth
from v1.billing.models.bill_cycle import BillCycle
from v1.billing.models.bill_frequency import BillFrequency
from v1.billing.models.bill_schedule import ScheduleBill
from v1.billing.models.additional_charges import AdditionalCharges
from v1.billing.models.tax import Tax
from v1.billing.models.rate import Rate
from v1.billing.models.bill import Bill
from v1.billing.models.bill_consumer_detail import BillConsumerDetail
from v1.billing.models.bill_schedule_log import ScheduleBillLog
from v1.billing.models.fixed_charges import FixedCharges
from v1.billing.models.invoice_template import InvoiceTemplate

admin.site.register(BillMonth)
admin.site.register(BillCycle)
admin.site.register(BillFrequency)
admin.site.register(ScheduleBill)
admin.site.register(AdditionalCharges)
admin.site.register(Tax)
admin.site.register(Rate)
admin.site.register(Bill)
admin.site.register(BillConsumerDetail)
admin.site.register(ScheduleBillLog)
admin.site.register(FixedCharges)
admin.site.register(InvoiceTemplate)