# table header
# module:  
# table type : Master
# table name : Mandatory Fields
# table description :  It will contain details for Product
# frequency of data changes : Low
# sample table data : "Activate", "Deactive"
# reference tables :
# author : Priyanka
# created on : 12/10/2020


from datetime import datetime  # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime

# Create Product table start

class Product(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def get_product_by_id(id):
    try:
        return Product.objects.get(id=id)
    except Exception as e:
        raise CustomAPIException("Product does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_product_by_id_string(id_string):
    try:
        return Product.objects.get(id_string=id_string)
    except:
        return False

# Create Product table end
