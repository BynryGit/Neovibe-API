from django.contrib import admin
from v1.utility.models.utility_module import UtilityModule
from v1.utility.models.utility_sub_module import UtilitySubModule

admin.site.register(UtilityModule)
admin.site.register(UtilitySubModule)