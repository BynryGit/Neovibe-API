from datetime import datetime # importing package for datetime
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.contrib.postgres.fields import JSONField

# Create Service Master table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class ServiceAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sa_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    # assignment_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    # assignment_time = models.TimeField()
    # completion_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    # completion_time = models.TimeField()
    # TAT = models.BigIntegerField(null=True, blank=True)
    # remark = models.CharField(max_length=200, blank=True, null=True)
    # status = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.sa_id

    def __unicode__(self):
        return self.sa_id
