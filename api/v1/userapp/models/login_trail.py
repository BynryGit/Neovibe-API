import uuid
from datetime import datetime

from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# table header
# module: Admin | sub-module - Login
# table type: transactional
# table name: 2.12.44 Portion (Local)
# table description: It contains the list of user login
# #frequency of data changes: high
# sample table data:
# reference tables: User
# Author: Arpita
# creation date:


class LoginTrail(models.Model): # change name to role
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.CharField(max_length=200,blank=False, null=False)
    status = models.CharField(max_length=200,blank=False, null=False)
    login_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    logout_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email