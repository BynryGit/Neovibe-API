import uuid
from datetime import datetime
from v1.utility.models.utility_product import UtilityProduct
from django.db import models
from v1.complaint.models.complaint_sub_type import get_complaint_sub_type_by_id
from v1.complaint.models.complaint_type import get_complaint_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField


class ConsumerComplaintMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    service_obj = JSONField(default='')
    complaint_type_id = models.BigIntegerField(null=True, blank=True)
    complaint_sub_type_id = models.BigIntegerField(null=True, blank=True)
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
    def get_complaint_type(self):
        return get_complaint_type_by_id(self.complaint_type_id)

    @property
    def get_complaint_sub_type(self):
        return get_complaint_sub_type_by_id(self.complaint_sub_type_id)


def get_consumer_complaint_master_by_id_string(id_string):
    try:
        return ConsumerComplaintMaster.objects.get(id_string=id_string)
    except:
        return False

