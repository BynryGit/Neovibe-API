import datetime
import uuid

from django.db import models
# Table Type : Lookup
# Table Name : 2.12.10 Unit
# Description :It captures Unit and ID of various Unit to be used by Operator or Utility
# Frequency of data changes : Low
# Reference Table : 2.2.2 Service Plans, Work order line items, 2.4.5 SOP details, 2.4.8 Asset maIntegerFieldenance details.
# Auther : Jayshree
# Creation Date : 21-04-2020


class Unit(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    unit = models.CharField(max_length=20, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.unit

    def __unicode__(self):
        return self.unit

