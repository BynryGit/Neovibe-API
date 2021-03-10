import uuid
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
# from v1.utility.models.utility_master import UtilityMaster


class EmailConfiguration(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey('utility.UtilityMaster', blank=True, null=True, on_delete=models.SET_NULL)
    email_port = models.CharField(max_length = 200, null = True, blank = True)
    email_backend = models.CharField(max_length = 200, null = True, blank = True)
    email_host = models.CharField(max_length = 200, null = True, blank = True)
    email_host_user = models.CharField(max_length = 200, null = True, blank = True)
    from_email = models.CharField(max_length = 200, null = True, blank = True)

    def __str__(self):
        return self.utility.name

    def __unicode__(self):
        return self.utility.name