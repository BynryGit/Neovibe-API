import datetime
import uuid

from django.db import models
from api.v1.smart360_API.lookup.models.activity import Activity


# Create Consumer Lookup - Portion (Local)
class Portion(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #TODO: remove _id: Done
    tenant = models.ForeignKey(TenantMaster,null=False, blank=False)  #Table name : Done
    utility = models.ForeignKey(UtilityMaster,null=False, blank=False)  # Table name:Done
    portion_name = models.CharField(null=False, blank=False)#TODO: Name: Done
    city_id = models.IntegerField(null=False, blank=False) #TODO: remove foreignkey :Done
    created_by = models.IntegerField(null=False, blank=False) #TODO: remove foreignkey : Done
    updated_by = models.IntegerField(null=False, blank=False) #TODO: remove foreignkey : Done
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)
