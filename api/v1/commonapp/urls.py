from django.urls import path
from v1.commonapp.views.role import RoleType, RoleSubType, FormFactor, Department

urlpatterns = [
    path('roletype/', RoleType.as_view()),
    path('rolesubtypes/', RoleSubType.as_view()),
    path('departments/', FormFactor.as_view()),
    path('submodules/', Department.as_view())
]