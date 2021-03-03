import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_product import get_utility_product_by_id


class ComplaintType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_utility_product(self):
        utility_product = get_utility_product_by_id(self.utility_product_id)
        return utility_product


def get_complaint_type_by_id_string(id_string):
    try:
        return ComplaintType.objects.get(id_string = id_string)
    except:
        return False


def get_complaint_type_by_id(id):
    try:
        return ComplaintType.objects.get(id=id)
    except:
        return False