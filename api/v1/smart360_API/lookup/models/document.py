import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.13 Document
# Description : This table will store Document Name. It captures Document Name and ID of various Document to be used by Operator or Utility.
# Frequency of data changes : Low
# Reference Table : 2.3.3 Survey Transaction Table, 2.3.8 Campaign Transaction Table, 2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.7.1. Employee, 2.5.5 User Documents.
# Auther : Jayshree
# Creation Date : 21-04-2020


class Document(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    document_name = models.CharField(max_length=40, blank=False, null=False)
    document_type_id = models.IntegerField(blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.document_name

    def __unicode__(self):
        return self.document_name
