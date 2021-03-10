import uuid
from datetime import datetime
import fsm
from django.db import models

from v1.payment.models.payment_sub_type import get_payment_sub_type_by_id
from v1.payment.models.payment_type import get_payment_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


class PaymentTransaction(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'SETTLED'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='payment_transaction_tenant')
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='payment_transaction_utility')
    identification_id = models.BigIntegerField(null=True, blank=True)
    transaction_type_id = models.BigIntegerField(null=True, blank=True)
    transaction_sub_type_id = models.BigIntegerField(null=True, blank=True)
    transaction_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=4)
    tax_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=4)
    transaction_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    state = models.BigIntegerField(choices=CHOICES, default=0)
    payment_id = models.BigIntegerField(null=True, blank=True)
    settlement_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=4)
    settlement_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __unicode__(self):
        return str(self.utility)

    def __str__(self):
        return str(self.utility)

    @property
    def get_transaction_type(self):
        transaction_type = get_payment_type_by_id(self.transaction_type_id)
        return transaction_type

    @property
    def get_transaction_sub_type(self):
        transaction_sub_type = get_payment_sub_type_by_id(self.transaction_sub_type_id)
        return transaction_sub_type
