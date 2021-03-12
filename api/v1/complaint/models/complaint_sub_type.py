import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.complaint.models.complaint_type import get_complaint_type_by_id
from django.utils import timezone # importing package for datetime


class ComplaintSubType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    complaint_type_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    @property
    def get_complaint_type(self):
        complaint_type = get_complaint_type_by_id(self.complaint_type_id)
        return complaint_type


def get_complaint_sub_type_by_id_string(id_string):
    try:
        return ComplaintSubType.objects.get(id_string=id_string)
    except:
        return False


def get_complaint_sub_type_by_id(id):
    try:
        return ComplaintSubType.objects.get(id=id)
    except:
        return False