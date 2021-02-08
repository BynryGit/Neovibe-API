# Table Header
# Table Type : Lookup (Local)
# Table Name : Utility Service Request Type
# Description : Utility Service Request Types
# Author : Rohan
# Date : 04-02-2021


from datetime import datetime  # importing package for datetime

from v1.commonapp.models.service_request_sub_type import get_service_sub_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Service Type table start
from v1.utility.models.utility_service_request_type import get_utility_service_request_type_by_id


class UtilityServiceRequestSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility_service_request_type_id = models.BigIntegerField(null=True, blank=True)
    service_request_sub_type_id = models.BigIntegerField(null=True, blank=True)
    label = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def __unicode__(self):
        return self.label

    property

    def get_utility_service_request_type(self):
        try:
            type = get_utility_service_request_type_by_id(self.utility_service_request_type_id)
            return type
        except:
            return False

    @property
    def get_service_request_sub_type(self):
        try:
            sub_type = get_service_sub_type_by_id(self.service_request_sub_type_id)
            return sub_type
        except:
            return False


def get_utility_service_request_sub_type_by_id_string(id_string):
    try:
        return UtilityServiceRequestSubType.objects.get(id_string=id_string)
    except:
        return False


def get_utility_service_request_sub_type_by_id(id):
    try:
        return UtilityServiceRequestSubType.objects.get(id=id)
    except:
        return False

# End the Code
