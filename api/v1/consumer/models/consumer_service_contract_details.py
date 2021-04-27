import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.meter_data_management.models.meter import get_meter_by_id
from v1.commonapp.models.transition_configuration import TRANSITION_CONFIGURATION_DICT
from v1.commonapp.views.custom_exception import CustomAPIException
import fsm
from django.utils import timezone # importing package for datetime


CONSUMER_DICT = {
    "CONNECTED": 0,
    "DISCONNECTED": 1,
    "CREATED": 2,
    "APPROVED": 3,
    "REJECTED":4,
    "HOLD":5
}

class ConsumerServiceContractDetail(models.Model, fsm.FiniteStateMachineMixin):
    STATUS = (
        (0, 'CONNECTED'),
        (1, 'DISCONNECTED'),
        (2, 'CREATED'),
        (3, 'APPROVED'),
        (4, 'REJECTED'),
        (5, 'HOLD')
    )

    state_machine = {
        CONSUMER_DICT['CREATED']: (CONSUMER_DICT['APPROVED'],CONSUMER_DICT['REJECTED'],CONSUMER_DICT['HOLD'], CONSUMER_DICT['CREATED']),
        CONSUMER_DICT['APPROVED']: (CONSUMER_DICT['HOLD'], CONSUMER_DICT['CONNECTED']),
        CONSUMER_DICT['CONNECTED']: (CONSUMER_DICT['DISCONNECTED']),
        CONSUMER_DICT['HOLD']: (CONSUMER_DICT['APPROVED'],CONSUMER_DICT['REJECTED']),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    service_contract_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    meter_id = models.BigIntegerField(null=True, blank=True)
    state = models.IntegerField(choices=STATUS, default=2)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.consumer_no)

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
        try:
            meter = get_meter_by_id(self.meter_id)
            return meter
        except:
            return False    


    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as e:
            raise CustomAPIException("Consumer transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)    


def get_consumer_service_contract_detail_by_id(id):
    try:
        return ConsumerServiceContractDetail.objects.get(id=id, is_active=True)
    except:
        return False


def get_consumer_service_contract_detail_by_id_string(id_string):
    try:
        return ConsumerServiceContractDetail.objects.get(id_string=id_string)
    except:
        return False


def get_consumer_service_contract_detail_by_meter_id(meter_id):
    try:
        return ConsumerServiceContractDetail.objects.get(meter_id=meter_id, is_active=True)
    except:
        return False

def get_consumer_service_contract_detail_by_premise_id(premise_id):
    try:
        return ConsumerServiceContractDetail.objects.filter(premise_id=premise_id, is_active=True).last()
    except:
        return False

def get_consumer_service_contract_detail_by_consumer_id(consumer_id):
    try:
        return ConsumerServiceContractDetail.objects.filter(consumer_id=consumer_id, is_active=True).last()
    except:
        return False