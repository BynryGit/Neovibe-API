from django.urls import path

from v1.commonapp.views.department import Department, DepartmentList
from v1.commonapp.views.form_factor import FormFactor, FormFactorList
from v1.commonapp.views.role_sub_type import RoleSubType, RoleSubTypeList
from v1.commonapp.views.role_type import RoleType, RoleTypeList
from v1.commonapp.views.sub_modules import SubModule, SubModuleList

urlpatterns = [
    path('role_type/', RoleType.as_view()),
    path('role_type/list/', RoleTypeList.as_view()),
    path('role_subtype/', RoleSubType.as_view()),
    path('role_subtype/list/', RoleSubTypeList.as_view()),
    path('form_factors/', FormFactor.as_view()),
    path('form_factor/list/', FormFactorList.as_view()),
    path('department/', Department.as_view()),
    path('department/list/', DepartmentList.as_view()),
    path('submodule/', SubModule.as_view()),
    path('submodule/list/', SubModuleList.as_view())
]