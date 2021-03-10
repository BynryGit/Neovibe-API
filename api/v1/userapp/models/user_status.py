import uuid
from datetime import datetime

from django.db import models

from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


class UserStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility


def get_user_status_by_id_string(id_string):
    try:
        return UserStatus.objects.get(id_string=id_string)
    except:
        return False


def get_user_status_by_id(id):
    return UserStatus.objects.filter(id=id).last()