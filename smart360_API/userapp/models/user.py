__author__ = "aki"

import uuid
from django.db import models
from django.contrib.auth.models import User


class User(User):
    """"Database Model For User In The System"""
    USER_STATUS = (
        (0, 'ACTIVE'),
        (1, 'INACTIVE'),
    )

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=500, null=True, blank=True)
    user_status = models.IntegerField(choices=USER_STATUS, null=False, blank=False, default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username
