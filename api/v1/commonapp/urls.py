from django.urls import path
from v1.commonapp.views.city import CityList
from v1.commonapp.views.country import CountryList
from v1.commonapp.views.region import RegionList
from v1.commonapp.views.state import StateList
from v1.commonapp.views.area import AreaList, AreaDetail
from v1.commonapp.views.department import Department, DepartmentList
from v1.commonapp.views.form_factor import FormFactor, FormFactorList
from v1.commonapp.views.sub_area import SubAreaList, SubAreaDetail
from v1.commonapp.views.sub_modules import SubModule, SubModuleList
from v1.commonapp.views.frequency import FrequencyList,FrequencyDetail
# from v1.userapp.views.role_sub_type import RoleSubType, RoleSubTypeList
# from v1.userapp.views.role_type import RoleType, RoleTypeList

urlpatterns = [
    path('area/<uuid:id_string>', AreaDetail.as_view()),
    path('area/list', AreaList.as_view()),
    path('sub_area/<uuid:id_string>', SubAreaDetail.as_view()),
    path('sub_area/list', SubAreaList.as_view()),
    path('frequency/list', FrequencyList.as_view()),
    path('frequency/<uuid:id_string>', FrequencyDetail.as_view()),
    # path('role_type/<uuid:id_string>', RoleType.as_view()),
    # path('role_type/list', RoleTypeList.as_view()),
    # path('role_subtype/<uuid:id_string>', RoleSubType.as_view()),
    # path('role_subtype/list', RoleSubTypeList.as_view()),
    path('form_factors', FormFactor.as_view()),
    path('form_factor/list', FormFactorList.as_view()),
    path('department/<uuid:id_string>', Department.as_view()),
    path('department/list', DepartmentList.as_view()),
    path('submodule/<uuid:id_string>', SubModule.as_view()),
    path('submodule/list/', SubModuleList.as_view()),
    # This api used for utility dropdown start
    path('regions', RegionList.as_view(), name='regions_list'),
    path('countries', CountryList.as_view(), name='country_list'),
    path('states', StateList.as_view(), name='state_list'),
    path('cities', CityList.as_view(), name='city_list'),
    # This api used for utility dropdown end
]