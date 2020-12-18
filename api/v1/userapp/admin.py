from django.contrib import admin

from v1.userapp.models.login_trail import LoginTrail
from v1.userapp.models.privilege import Privilege
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.role_sub_type import RoleSubType
from v1.userapp.models.role_type import RoleType
from v1.userapp.models.user_area import UserArea
from v1.userapp.models.user_bank import UserBank
from v1.userapp.models.user_mobile import UserDetails
from v1.userapp.models.user_privilege import UserPrivilege
from v1.userapp.models.user_role import UserRole
from v1.userapp.models.role import Role
from v1.userapp.models.user_skill import UserSkill
from v1.userapp.models.user_status import UserStatus
from v1.userapp.models.user_sub_type import UserSubType
from v1.userapp.models.user_token import UserToken
from v1.userapp.models.user_type import UserType
from v1.userapp.models.user_utility import UserUtility
from v1.userapp.models.user_leaves import UserLeaves
from v1.userapp.models.user_detail import UserDetail
from v1.userapp.models.field_agent_live_location import FieldAgentLiveLocation

admin.site.register(UserToken)
admin.site.register(LoginTrail)
admin.site.register(Privilege)
admin.site.register(Role)
admin.site.register(RolePrivilege)
admin.site.register(UserPrivilege)
admin.site.register(UserUtility)
admin.site.register(UserSkill)
admin.site.register(UserArea)
admin.site.register(UserBank)
# admin.site.register(UserDetails)
admin.site.register(UserRole)
admin.site.register(UserType)
admin.site.register(UserSubType)
admin.site.register(RoleSubType)
admin.site.register(RoleType)
admin.site.register(UserStatus)
admin.site.register(UserLeaves)
admin.site.register(UserDetail)
admin.site.register(FieldAgentLiveLocation)
