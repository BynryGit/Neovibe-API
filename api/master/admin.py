from django.contrib import admin
from master.models import User
from master.models import User,MasterUser


# Register your models here.

admin.site.register(MasterUser)
admin.site.register(User)
