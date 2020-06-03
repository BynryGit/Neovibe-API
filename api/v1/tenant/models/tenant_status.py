from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database

#Create Tenant Status


class TenantStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def get_tenant_status_by_id_string(id_string):
    return TenantStatus.objects.get(id_string = id_string)


def get_tenant_status_by_id(id):
    return TenantStatus.objects.get(id=id)


def get_tenant_statuses_by_tenant_id_string(id_string):
    return TenantStatus.objects.filter(tenant__id_string=id_string, is_active=True)
