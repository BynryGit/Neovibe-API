from django.urls import path

from v1.userapp.views.bank_detail import Bank, BankList, GetBankList
from v1.userapp.views.document import Document
from v1.userapp.views.notes import Note
from v1.userapp.views.role import RoleList, PrivilegeDetail, Role, GetRoleList
from v1.userapp.views.skills import SkillList
from v1.userapp.views.user import Users, UserList, UserRole

urlpatterns = [
    path('role/', Role.as_view()),
    path('role/<uuid:id_string>', Role.as_view()),
    path('roles/', GetRoleList.as_view()),
    path('list/', RoleList.as_view()),
    path('privileges/', PrivilegeDetail.as_view()),
    path('<uuid:id_string>', Users.as_view()),
    path('list/', UserList.as_view()),
    path('bank/list', BankList.as_view()),
    path('bank-detail/', GetBankList.as_view()),
    path('bank/<uuid:id_string>', Bank.as_view()),
    path('documents/<uuid:id_string>', Document.as_view()),
    path('notes/<uuid:id_string>', Note.as_view()),
    path('skills/<uuid:id_string>', SkillList.as_view()),
    path('privilege/<uuid:id_string>', UserRole.as_view()),
]