import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.14 Consumer Category
# Description : This table will store Consumer Category. It captures Consumer Category and ID of various Consumer Category to be used by Operator or Utility.
# Frequency of data changes : Low
# Reference Table : 2.2.2 Service Plans, 2.3.1 Survey Table, 2.3.8 Campaign Transaction Table, 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.4.3 Asset Master, 2.7.1. Employee.
# Auther : Jayshree
# Creation Date : 21-04-2020


class ConsumerCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    category_name = models.CharField(max_length=40, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

    def __unicode__(self):
        return self.category_name
