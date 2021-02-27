# Table Header
# module : All modules & sub-modules
# Table Type : Lookup (Global)
# Table Name : 2.12.13 Document
# Description : It is a global lookup tables that stores the names of the documents
# Frequency of data changes : Low
# Sample Table Data : "Aadhar Card", "Pan Card", "Passport"
# Reference Table : 2.3.3 Survey Transaction Table, 2.3.8 Campaign Transaction Table, 2.3.1. Consumer Master,
#                   2.3.2. Consumer - Registration, 2.7.1. Employee, 2.5.5 User Documents.
# Author : Rohan Wagh
# Creation Date : 24-10-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime

from v1.commonapp.models.document_sub_type import get_document_sub_type_by_id
from v1.utility.models.utility_document_type import get_utility_document_type_by_id
from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
# from v1.userapp.models.user_master import get_user_by_id

# from v1.userapp.models.user_master import get_user_by_id

from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database


# Create Document table start


class Document(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    object_id = models.BigIntegerField(null=True, blank=True)
    document_type_id = models.BigIntegerField(null=True, blank=True)
    document_sub_type_id = models.BigIntegerField(null=True, blank=True)
    document_generated_name = models.CharField(max_length=1000, blank=True, null=True)
    document_name = models.CharField(max_length=1000, blank=True, null=True)
    file_type = models.CharField(max_length=1000, blank=True, null=True)
    document_size = models.CharField(max_length=1000, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_by = models.BigIntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return str(self.document_generated_name)

    def __unicode__(self):
        return self.document_generated_name

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)

    @property
    def get_sub_module(self):
        return get_sub_module_by_id(self.sub_module_id)

    @property
    def get_utility_document_type(self):
        return get_utility_document_type_by_id(self.document_type_id)

    @property
    def get_sub_type(self):
        return get_document_sub_type_by_id(self.document_sub_type_id)

    @property
    def get_user_identification(self):
        # return get_user_by_id(self.identification_id)
        return True


# Create Document table end


def get_documents_by_utility_id_string(id_string):
    return Document.objects.filter(utility__id_string=id_string)


def get_documents_by_tenant_id_string(id_string):
    return Document.objects.filter(tenant__id_string=id_string)


def get_documents_by_user_id(id):
    return Document.objects.filter(object_id=id)


def get_document_by_id_string(id_string):
    try:
        return Document.objects.get(id_string=id_string)
    except:
        return False


def get_document_by_id(id):
    return Document.objects.filter(id=id).last()


def get_document_by_user_id(user_id, document_type_id):
    return Document.objects.filter(object_id=user_id, document_type_id=document_type_id)
