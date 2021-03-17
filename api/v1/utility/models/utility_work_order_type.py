# Table Header
# Table Type : Lookup (Local)
# Table Name : Utility Work Order Type
# Description : Utility Work Order Types
# Author : Chetan Dhongade
# Date : 18/02/21


from datetime import datetime # importing package for datetime

from v1.commonapp.models.work_order_type import get_work_order_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create Utility work order Type table start

class UtilityWorkOrderType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    work_order_type_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_work_order_type(self):
        try:
            type = get_work_order_type_by_id(self.work_order_type_id)
            return type
        except:
            return False

# Create Utility work_order Type table end


def get_utility_work_order_type_by_id_string(id_string):
    try:
        return UtilityWorkOrderType.objects.get(id_string=id_string)
    except:
        return False


def get_utility_work_order_type_by_id(id):
    try:
        return UtilityWorkOrderType.objects.get(id=id)
    except:
        return False

# End the Code
