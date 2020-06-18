from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database

#Create Tenant Status start


class TenantStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

#Create Tenant Status end


def get_tenant_status_by_id(id):
    try:
        return TenantStatus.objects.get(id=id)
    except:
        return False


def get_tenant_status_by_id_string(id_string):
    try:
        return TenantStatus.objects.get(id_string=id_string)
    except:
        return False

