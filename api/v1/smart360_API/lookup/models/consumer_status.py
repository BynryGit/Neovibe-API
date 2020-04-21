import datetime
import uuid

from django.db import models
from api.v1.smart360_API.lookup.models.activity import Activity


# Create Consumer Lookup - Portion (Local)
class Consumer_status(models.Model):
    portion_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    id_string = models.CharField(null=False, blank=False)
    tenant_id = models.ForeignKey(null=False, blank=False)
    utility_id = models.ForeignKey(null=False, blank=False)
    portion = models.CharField(null=False, blank=False)
    city_id = models.ForeignKey(null=False, blank=False)
    created_by = models.ForeignKey(null=False, blank=False)
    updated_by = models.ForeignKey(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)
