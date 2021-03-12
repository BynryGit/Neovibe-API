import uuid
from datetime import datetime
from django.db import models

from v1.consumer.models.consumer_offer_master import get_consumer_offer_master_by_id
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class ConsumerOfferDetail(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    offer_id = models.BigIntegerField(null=True, blank=True)
    consumer_service_contract_detail_id = models.BigIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    end_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.utility.name

    def __unicode__(self):
        return self.utility.name

    @property
    def get_offer(self):
        try:
            offer = get_consumer_offer_master_by_id(self.offer_id)
            return offer
        except:
            return False

    @property
    def get_consumer_service_contract_detail(self):
        try:
            consumer_service_contract_detail = get_consumer_service_contract_detail_by_id(self.consumer_service_contract_detail_id)
            return consumer_service_contract_detail
        except:
            return False
