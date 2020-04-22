# Table Header : Skills
# Table Type : Lookup (Local)
# Table Name : 2.12.76 Skills
# Description : It will store the skills of each service type.
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.6.1 Service Request
# Auther : Jayshree
# Creation Date : 22/04/2020


import datetime
import uuid
from django.db import models

# Start the Code
class Skills(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    skill = models.CharField(max_length=30, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    service_type_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.skill

    def __unicode__(self):
        return self.skill
# End The Code