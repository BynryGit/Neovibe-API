from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class RouteDetail(models.Model):
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    route_code = models.CharField(max_length=200, blank=True, null=True)
    bill_month = models.CharField(max_length=200, blank=True, null=True)
    bill_cycle_id = models.BigIntegerField(blank=True, null=True)
    billing_status_id = models.BigIntegerField(blank=True, null=True)
    route_id = models.BigIntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(default=datetime.utcnow())
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.route_code