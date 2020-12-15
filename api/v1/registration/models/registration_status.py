from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database
from v1.registration.models.registrations import Registration as RegTbl


# Create Registration Type table start
class RegistrationStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    state = models.BigIntegerField(choices=RegTbl.CHOICES, default=0)
    ui_class = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# def get_registration_status_by_id_string(id_string):
#     try:
#         return RegistrationStatus.objects.get(id_string = id_string)
#     except:
#         return False


# def get_registration_status_by_id(id):
#     return RegistrationStatus.objects.get(id = id)


# def get_registration_statuses_by_tenant_id_string(id_string):
#     return RegistrationStatus.objects.filter(tenant__id_string = id_string, is_active = True)
