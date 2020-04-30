from django.contrib import admin
from v1.userapp.models.privilege import Privilege
from v1.userapp.models.role import Role
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.user_areas import UserArea
from v1.userapp.models.user_master import SystemUser
from v1.userapp.models.user_mobile import UserDetails
from v1.userapp.models.user_privilege import UserPrivilege
from v1.userapp.models.user_skills import UserSkills
from v1.userapp.models.user_token import UserToken
from v1.userapp.models.user_type import UserType

admin.site.register(UserToken)
admin.site.register(Privilege)
admin.site.register(Role)
admin.site.register(RolePrivilege)
admin.site.register(UserSkills)
admin.site.register(UserArea)
admin.site.register(SystemUser)
admin.site.register(UserDetails)
admin.site.register(UserPrivilege)
admin.site.register(UserType)