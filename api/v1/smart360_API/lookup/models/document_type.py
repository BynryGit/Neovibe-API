# Table Header : Document Type
# Table Type : Lookup (Global)
# Table Name : 2.12.12 Document Type
# Description : This table will store Document Type with respect to Document name.
# Frequency of data changes : Low
# Sample Table Data : ID Proof, Address Proof
# Reference Table : 2.3.3 Survey Transaction Table, 2.3.8 Campaign Transaction Table, 2.3.1. Consumer Master,
#                    2.3.2. Consumer - Registration, 2.7.1. Employee, 2.5.5 User Documents.
# Auther : Jayshree
# Creation Date : 21-04-2020
import datetime
import uuid
from django.db import models

# Start the Code
class DocumentType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    document_type = models.CharField(max_length=20, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.document_type

    def __unicode__(self):
        return self.document_type
# End The Code