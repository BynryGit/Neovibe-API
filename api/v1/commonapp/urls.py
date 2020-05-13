from django.urls import path
from v1.commonapp.views.area import AreaList, AreaView
from v1.commonapp.views.department import Department, DepartmentList
from v1.commonapp.views.form_factor import FormFactor, FormFactorList
from v1.commonapp.views.role_sub_type import RoleSubType, RoleSubTypeList
from v1.commonapp.views.role_type import RoleType, RoleTypeList
from v1.commonapp.views.sub_area import SubAreaView, SubAreaList
from v1.commonapp.views.sub_modules import SubModule, SubModuleList

urlpatterns = [
    path('area/<uuid:id_string>', AreaView.as_view()),
    path('area/list', AreaList.as_view()),
    path('sub_area/<uuid:id_string>', SubAreaView.as_view()),
    path('sub_area/list', SubAreaList.as_view()),
    path('role_type/<uuid:id_string>', RoleType.as_view()),
    path('role_type/list', RoleTypeList.as_view()),
    path('role_subtype/<uuid:id_string>', RoleSubType.as_view()),
    path('role_subtype/list', RoleSubTypeList.as_view()),
    path('form_factors', FormFactor.as_view()),
    path('form_factor/list', FormFactorList.as_view()),
    path('department/<uuid:id_string>', Department.as_view()),
    path('department/list', DepartmentList.as_view()),
    path('submodule/<uuid:id_string>', SubModule.as_view()),
    path('submodule/list/', SubModuleList.as_view())
]