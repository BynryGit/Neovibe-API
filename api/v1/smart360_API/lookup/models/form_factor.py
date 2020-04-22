# Table Header : Form Factor
# Table Type : Lookup (Global)
# Table Name : 2.12.18 Form Factor
# Description : It capture form factor and ID of various form factor to be used by Operator or Utility
# Sample Table Data : Web, Mobile
# Frequency of data changes : Low
# Reference Table : 2.4.6. Consumer Token
# Auther : Jayshree
# Creation Date : 21-04-2020

import datetime
import uuid
from django.db import models

# Start the code
class FormFactor(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    form_factor = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.form_factor

    def __unicode__(self):
        return self.form_factor
# End the code