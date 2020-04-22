import datetime
import uuid

from django.db import models
from api.v1.smart360_API.lookup.models.activity import Activity
#TODO: correct the spelling :Done
# Create Consumer Registration table start.
class Privilege(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    privilege = models.CharField(null=False, blank=False)
    activity = models.ForeignKey(Activity,null=False, blank=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.privilege

    def __unicode__(self):
        return self.privilege



def get_privilege_by_id(id):
    return Privilege.objects.get(id=id)