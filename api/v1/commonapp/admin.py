from django.contrib import admin
from v1.commonapp.models.area import Area
from v1.commonapp.models.city import City
from v1.commonapp.models.country import Country
from v1.commonapp.models.department import Department
from v1.commonapp.models.form_factor import FormFactor
from v1.commonapp.models.module import Module
from v1.commonapp.models.region import Region
from v1.commonapp.models.state import State
from v1.commonapp.models.sub_area import SubArea
from v1.commonapp.models.sub_module import SubModule

admin.site.register(Region)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Module)
admin.site.register(SubModule)
admin.site.register(Area)
admin.site.register(SubArea)
admin.site.register(Department)
admin.site.register(FormFactor)