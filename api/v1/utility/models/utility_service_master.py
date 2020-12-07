import uuid
from datetime import datetime
from django.db import models


class UtilityServiceMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    service_name = models.CharField(max_length=200, blank=True, null=True) # Gas, Water, Power
    service_description = models.CharField(max_length=500, blank=True, null=True)
    service_type_id = models.BigIntegerField(null=True, blank=True)
    service_sub_type_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.service_name

    def __unicode__(self):
        return self.service_name


def get_service_master_by_id(id):
    try:
        return UtilityServiceMaster.objects.get(id=id)
    except:
        return False
