import uuid
from datetime import datetime
from django.db import models
from v1.consumer.models.offer_type import get_offer_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class OfferSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    offer_type_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_offer_type(self):
        offer_type = get_offer_type_by_id(self.offer_type_id)
        return offer_type


def get_offer_sub_type_by_id_string(id_string):
    try:
        return OfferSubType.objects.get(id_string=id_string)
    except:
        return False


def get_offer_sub_type_by_id(i_d):
    try:
        return OfferSubType.objects.get(id=i_d)
    except:
        return False
