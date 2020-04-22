import datetime
import uuid

from django.db import models

# Table Type : Lookup
# Table Name : 2.12.11 Currency
# Description : It captures Currency and ID of various Currency to be used by Operator or Utility
# Frequency of data changes : Low
# Reference Table : 2.2.2 Service Plans, 2.3.13. Consumer - Payments, 2.5.2 Contracts Table
# Auther : Jayshree
# Creation Date : 21-04-2020


class Currency(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    currency = models.CharField(max_length=20, blank=False, null=False)
    country_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.currency

    def __unicode__(self):
        return self.currency

