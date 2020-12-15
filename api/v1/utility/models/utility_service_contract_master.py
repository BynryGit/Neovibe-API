import uuid
from datetime import datetime
from django.db import models
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_service import get_utility_service_by_id


class UtilityServiceContractMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    service_id = models.BigIntegerField(null=True, blank=True)
    deposite_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=4)
    consumer_category_id = models.BigIntegerField(null=True, blank=True)
    consumer_sub_category_id = models.BigIntegerField(null=True, blank=True)
    service_contract_template_id = models.BigIntegerField(null=True, blank=True)
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
    def get_service(self):
        service = get_utility_service_by_id(self.service_id)
        return service

    @property
    def get_consumer_category(self):
        category = get_consumer_category_by_id(self.consumer_category_id)
        return category

    @property
    def get_consumer_sub_category(self):
        sub_category = get_consumer_sub_category_by_id(self.consumer_sub_category_id)
        return sub_category


def get_utility_service_contract_master_by_id_string(id_string):
    try:
        return UtilityServiceContractMaster.objects.get(id_string=id_string)
    except:
        False


def get_utility_service_contract_master_by_id(id):
    try:
        return UtilityServiceContractMaster.objects.get(id=id)
    except:
        False
