import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class AuditLog(models.Model):

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    object_id = models.BigIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=1000, blank=True, null=True)
    old_value = models.CharField(max_length=1000, blank=True, null=True)
    new_value = models.CharField(max_length=1000, blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)
    log_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.new_value

    def __unicode__(self):
        return self.new_value
