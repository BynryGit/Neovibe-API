import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class ConsumerOfferMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    offer_name = models.CharField(max_length=200, null=True, blank=True)
    offer_type_id = models.BigIntegerField(null=True, blank=True)
    offer_sub_type_id = models.BigIntegerField(null=True, blank=True)
    offer_code = models.CharField(max_length=200, null=True, blank=True)
    offer_image = models.CharField(max_length=200, null=True, blank=True)
    offer_max_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    offer_percentage = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    description = models.CharField(max_length=2000, null=True, blank=True)
    effective_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    expiry_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.offer_code

    def __unicode__(self):
        return self.offer_code