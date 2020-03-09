import uuid
from datetime import datetime
from django.db import models
from userapp.models.user import User


class Privilege(models.Model):
    """"Database Model For Privilege In The System"""

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # tenant_id = models.ForeignKey()
    # utility_id = models.ForeignKey()
    # activity_id = models.ForeignKey()
    name = models.CharField(null=False, blank=False)
    description = models.CharField(null=True, blank=True)
    created_by = models.ForeignKey(User)
    updated_by = models.ForeignKey(User)
    created_date = models.DateTimeField(default=datetime.now())
    updated_date = models.DateTimeField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name