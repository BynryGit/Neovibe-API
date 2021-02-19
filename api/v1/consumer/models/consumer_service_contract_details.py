import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.meter_data_management.models.meter import get_meter_by_id


class ConsumerServiceContractDetail(models.Model):
    STATUS = (
        (0, 'CONNECTED'),
        (1, 'DISCONNECTED'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    service_contract_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    meter_id = models.BigIntegerField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

    @property
    def get_contract(self):
        try:
            contract = get_utility_service_contract_master_by_id(self.service_contract_id)
            return contract
        except:
            return False

    @property
    def get_consumer_number(self):
        consumer = get_consumer_by_id(self.consumer_id)
        return consumer

    @property
    def get_meter_number(self):
        meter = get_meter_by_id(self.meter_id)
        return meter


def get_consumer_service_contract_detail_by_id(id):
    try:
        return ConsumerServiceContractDetail.objects.get(id=id, is_active=True)
    except:
        return False


def get_consumer_service_contract_detail_by_id_string(id_string):
    try:
        return ConsumerServiceContractDetail.objects.get(id_string=id_string, is_active=True)
    except:
        return False
