import uuid
from datetime import datetime

from django.db import models  # importing package for database


class LoginTrail(models.Model): # change name to role
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=200,blank=False, null=False)
    password = models.CharField(max_length=200,blank=False, null=False)
    status = models.CharField(max_length=200,blank=False, null=False)
    login_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    logout_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username