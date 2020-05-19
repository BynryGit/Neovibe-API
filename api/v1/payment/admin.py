from django.contrib import admin
from v1.payment.models.consumer_payment import Payment
from v1.payment.models.payment_channel import PaymentChannel
from v1.payment.models.payment_mode import PaymentMode
from v1.payment.models.payment_source import PaymentSource
from v1.payment.models.payment_sub_type import PaymentSubType
from v1.payment.models.payment_type import PaymentType

admin.site.register(Payment)
admin.site.register(PaymentChannel)
admin.site.register(PaymentMode)
admin.site.register(PaymentSource)
admin.site.register(PaymentSubType)
admin.site.register(PaymentType)