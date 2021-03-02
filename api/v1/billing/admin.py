from django.contrib import admin
from v1.billing.models.bill_month import BillMonth
from v1.billing.models.bill_cycle import BillCycle
from v1.billing.models.bill_frequency import BillFrequency
from v1.billing.models.schedule_bill import ScheduleBill
from v1.billing.models.additional_charges import AdditionalCharges
from v1.billing.models.tax import Tax
from v1.billing.models.rate import Rate
from v1.billing.models.bill import Bill

admin.site.register(BillMonth)
admin.site.register(BillCycle)
admin.site.register(BillFrequency)
admin.site.register(ScheduleBill)
admin.site.register(AdditionalCharges)
admin.site.register(Tax)
admin.site.register(Rate)
admin.site.register(Bill)