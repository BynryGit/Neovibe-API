from django.urls import path

from v1.userapp.views.bank_detail import Bank, BankList, GetBankList
from v1.userapp.views.document import Document, UserDocument
from v1.userapp.views.notes import UserNote
from v1.userapp.views.skills import SkillList
from v1.userapp.views.user import User, UserList, UserRole, UserDetail, UserBankDetail

urlpatterns = [
    path('', User.as_view()),
    path('<uuid:id_string>', UserDetail.as_view()),
    path('list/', UserList.as_view()),

    path('<uuid:id_string>/bank/', UserBankDetail.as_view()),

    path('<uuid:id_string>/role/', UserRole.as_view()),

    path('<uuid:id_string>/note/', UserNote.as_view()),

    path('<uuid:id_string>/document/', UserDocument.as_view()),

    path('bank/list', BankList.as_view()),
    path('bank-detail/', GetBankList.as_view()),
    path('bank/<uuid:id_string>', Bank.as_view()),
    path('documents/<uuid:id_string>', Document.as_view()),
    # path('notes/<uuid:id_string>', Note.as_view()),
    path('skills/<uuid:id_string>', SkillList.as_view()),
    path('privilege/<uuid:id_string>', UserRole.as_view()),
]