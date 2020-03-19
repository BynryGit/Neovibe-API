from django.contrib import admin
from userapp.models.user import User
from userapp.models.token import Token

admin.site.register(Token)
admin.site.register(User)
