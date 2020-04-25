# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.3. User Details
# table description : A master table that stores details of all users in the system.
# frequency of data changes : Low
# sample tale data : "user1", "user2"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create User Details table start

class UserDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    city = models.IntegerField(blank=False, null=False)
    first_name = models.CharFiaddeld(max_lengt=200, null=True, blank=True)
    middle_name = models.CharField(max_lengt=200, null=True, blank=True)
    last_name = models.CharField(max_lengt=200, null=True, blank=True)
    user_image = models.UrlField(null=True, blank=True)
    email_id = models.CharField(max_lengt=200, null=True, blank=True)
    password = models.CharField(max_lengt=200, null=True, blank=True)
    salt = models.CharField(max_lengt=200, null=False, blank=False)
    phone_no_1 = models.CharField(max_lengt=200, null=False, blank=False)
    phone_no_2 = models.CharField(max_lengt=200, null=False, blank=False)
    user_type = models.IntegerField(null=False, blank=False)
    department = models.IntegerField(null=True, blank=True)
    vendor = models.IntegerField(null=True, blank=True)
    emp_id = models.CharField(max_length=200, null=True, blank=True)
    imei_no = models.CharField(max_length=200, null=True, blank=True)
    role = models.IntegerField(null=True, blank=True)
    role_type = models.IntegerField(null=False, blank=False)
    form_factor = models.IntegerField(null=False, blank=False)
    data_access = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.id_string

    def __unicode__(self):
        return self.id_string

# Create User Details table end
