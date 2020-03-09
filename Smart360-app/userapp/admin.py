from django.contrib import admin
from userapp.models.user import User, Token

admin.site.register(Token)
admin.site.register(User)
