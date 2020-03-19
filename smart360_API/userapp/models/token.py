__author__ = "aki"

from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    """Database Model For User Token"""
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    token = models.CharField(max_length=1000, null=False, blank=False)