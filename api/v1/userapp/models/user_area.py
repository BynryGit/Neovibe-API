import uuid
from datetime import datetime

from django.db import models

from v1.commonapp.models.area import get_area_by_id_string
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.user_master import get_user_by_id_string


class UserArea(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name


def get_area_by_user_id(user_id):
    return UserArea.objects.filter(user_id=user_id, is_active=True)


def get_record_by_values(user_id_string,area_id_string):
    user = get_user_by_id_string(user_id_string)
    area = get_area_by_id_string(area_id_string)
    return UserArea.objects.filter(user_id=user.id,area_id=area.id).last()