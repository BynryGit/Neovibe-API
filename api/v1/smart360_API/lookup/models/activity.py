import datetime
import uuid

from django.db import models

# Create Consumer Registration table start.
class Activity(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    activity = models.CharField(null=False, blank=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)