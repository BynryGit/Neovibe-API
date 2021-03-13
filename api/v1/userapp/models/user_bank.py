import uuid
from datetime import datetime

from django.db import models

# from master.models import get_user_by_id_string
from master.models import get_user_by_id_string
from v1.tenant.models.tenant_bank_details import get_tenant_bank_details_by_id_string, get_tenant_bank_details_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime


class UserBank(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    bank_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name

    def get_tenant(self):
        return self.tenant

    def get_bank(self):
        return get_tenant_bank_details_by_id(self.bank_id)


def get_user_bank_by_user_id(user_id):
    try:
        return UserBank.objects.get(user_id=user_id, is_active=True)
    except:
        return False


def check_user_bank_exists(user_id_string):
    user_id = get_user_by_id_string(user_id_string)
    return UserBank.objects.filter(user_id=user_id.id, is_active=True).exists()


def get_record_by_values(user_id_string,bank_id_string):
    user = get_user_by_id_string(user_id_string)
    bank = get_tenant_bank_details_by_id_string(bank_id_string)
    return UserBank.objects.filter(user_id=user.id, area_id=bank.id, is_active=True).last()