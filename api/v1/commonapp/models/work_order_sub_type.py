import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from v1.commonapp.models.work_order_type import get_work_order_type_by_id


# Create WorkOrder Sub Type table start


class WorkOrderSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    work_order_type_id = models.BigIntegerField(null=True, blank=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def work_order_type(self):
        work_order_type = get_work_order_type_by_id(self.work_order_type_id)
        return work_order_type


def get_work_order_sub_type_by_id(id):
    try:
        return WorkOrderSubType.objects.get(id=id)
    except Exception as e:
        raise CustomAPIException("Work Order Sub Type does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_work_order_sub_type_by_id_string(id_string):
    try:
        return WorkOrderSubType.objects.get(id_string=id_string)
    except:
        return False


def get_work_order_sub_type_by_key(key):
    try:
        return WorkOrderSubType.objects.get(key=key)
    except:
        return False
# Create WorkOrderSubType table end.
