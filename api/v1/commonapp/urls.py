from django.urls import path

from v1.commonapp.views.department import Department, DepartmentList
from v1.commonapp.views.form_factor import FormFactor, FormFactorList
from v1.commonapp.views.role_type import RoleType, RoleSubType
from v1.commonapp.views.sub_modules import SubModule

urlpatterns = [
    path('role_type/', RoleType.as_view()),
    path('role_subtypes/', RoleSubType.as_view()),
    path('form_factors/', FormFactor.as_view()),
    path('form_factor/list/', FormFactorList.as_view()),
    path('departments/', Department.as_view()),
    path('department/list/', DepartmentList.as_view()),
    path('submodules/', SubModule.as_view())
]