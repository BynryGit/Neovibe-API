import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


class ConsumerDownPayment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    collected_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    remaining_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.collected_amount)

    def __unicode__(self):
        return self.collected_amount
