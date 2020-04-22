import datetime
import uuid

from django.db import models
from api.v1.smart360_API.lookup.models.activity import Activity

# It is sub module lookup up table. This table will save all the sub modules.Create Consumer Registration table start.
class SubModule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sub_module = models.CharField(null=False, blank=False)
    activity = models.ForeignKey(Activity,null=False, blank=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)