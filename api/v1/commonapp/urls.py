from django.urls import path
from v1.commonapp.views.city import CityList, City, CityDetail
from v1.commonapp.views.country import CountryList, Country, CountryDetail
from v1.commonapp.views.currency import CurrencyList
from v1.commonapp.views.region import RegionList, Region, RegionDetail
from v1.commonapp.views.state import StateList, State, StateDetail
from v1.commonapp.views.zone import ZoneList, Zone, ZoneDetail
from v1.commonapp.views.area import AreaList, AreaDetail, Area
from v1.commonapp.views.department import Department, DepartmentList
from v1.commonapp.views.form_factor import FormFactor, FormFactorList
from v1.commonapp.views.sub_area import SubAreaList, SubAreaDetail, SubArea
from v1.commonapp.views.module import ModuleList
from v1.commonapp.views.sub_modules import SubModule, SubModuleList
from v1.commonapp.views.frequency import FrequencyList,FrequencyDetail
from v1.commonapp.views.service_type import ServiceTypeList,ServiceTypeDetail
from v1.commonapp.views.products import ProductList
# from v1.userapp.views.role_sub_type import RoleSubType, RoleSubTypeList
from v1.userapp.views.role_type import RoleTypeList
from v1.commonapp.views.skills import SkillsList,SkillDetail,Skill
from v1.userapp.views.role_sub_type import RoleSubTypeByRoleType
from v1.commonapp.views.premises import PremiseList,Premise
from v1.commonapp.views.channel import ChannelList,Channel
from v1.commonapp.views.frequency import FrequencyDetail,FrequencyList,Frequency

urlpatterns = [
    path('utility/region', Region.as_view()),
    path('utility/region/<uuid:id_string>', RegionDetail.as_view()),
    path('utility/country', Country.as_view()),
    path('utility/country/<uuid:id_string>', CountryDetail.as_view()),
    path('utility/state', State.as_view()),
    path('utility/state/<uuid:id_string>', StateDetail.as_view()),
    path('utility/city', City.as_view()),
    path('utility/city/<uuid:id_string>', CityDetail.as_view()),
    path('utility/zone', Zone.as_view()),
    path('utility/zone/<uuid:id_string>', ZoneDetail.as_view()),
    path('utility/area', Area.as_view()),
    path('utility/area/<uuid:id_string>', AreaDetail.as_view()),
    path('utility/subarea', SubArea.as_view()),
    path('utility/subarea/<uuid:id_string>', SubAreaDetail.as_view()),
    path('utility/premise', Premise.as_view()),
    path('utility/skill/<uuid:id_string>', SkillDetail.as_view()),
    path('utility/skill', Skill.as_view()),
    path('sub_area/list', SubAreaList.as_view()),
    path('utility/<uuid:id_string>/frequency/list', FrequencyList.as_view()),
    path('utility/frequency/<uuid:id_string>', FrequencyDetail.as_view()),
    path('utility/frequency', Frequency.as_view()),
    path('product/list', ProductList.as_view()),
    # path('role_type/<uuid:id_string>', RoleType.as_view()),
    # path('role_type/list', RoleTypeList.as_view()),
    # path('role_subtype/<uuid:id_string>', RoleSubType.as_view()),
    # path('role_subtype/list', RoleSubTypeList.as_view()),
    path('form_factors', FormFactor.as_view()),
    path('form-factor/list', FormFactorList.as_view()),
    path('department/<uuid:id_string>', Department.as_view()),
    path('<uuid:id_string>/department/list', DepartmentList.as_view()),
    path('module/list', ModuleList.as_view()),
    path('submodule/<uuid:id_string>', SubModule.as_view()),
    path('submodule/list', SubModuleList.as_view()),
    # This api used for utility dropdown start
    path('region/list', RegionList.as_view(), name='regions_list'),
    path('channel/list', ChannelList.as_view(), name='channel_list'),
    path('utility/channel', Channel.as_view(), name='channel_add'),
    path('utility/<uuid:id_string>/country/list', CountryList.as_view(), name='country_list'),
    path('utility/<uuid:id_string>/state/list', StateList.as_view(), name='state_list'),
    path('utility/<uuid:id_string>/city/list', CityList.as_view(), name='city_list'),
    path('utility/<uuid:id_string>/zone/list', ZoneList.as_view(), name='zone_list'),
    path('utility/<uuid:id_string>/area/list', AreaList.as_view(), name='area_list'),
    path('utility/<uuid:id_string>/subarea/list', SubAreaList.as_view(), name='subarea_list'),
    path('utility/<uuid:id_string>/premise/list', PremiseList.as_view(), name='premise_list'),
    # This api used for utility dropdown end
    path('service_type/list', ServiceTypeList.as_view(), name="service_type_list"),
    path('service_type/<uuid:id_string>', ServiceTypeDetail.as_view(), name="service_type_detail"),
    path('<uuid:id_string>/areas', AreaList.as_view()),
    path('<uuid:id_string>/sub-areas', SubAreaList.as_view()),
    # path('<uuid:id_string>/cities', CityList.as_view()),
    path('<uuid:id_string>/states', StateList.as_view()),
    path('role-type/list', RoleTypeList.as_view()),
    path('utility/<uuid:id_string>/skill/list', SkillsList.as_view()),
    path('role-type/<uuid:id_string>/role-subtype/list', RoleSubTypeByRoleType.as_view(),name='utility_status_list'),
    path('<uuid:id_string>/state/list', StateList.as_view(), name='state_list'),


    path('currency/list', CurrencyList.as_view()),

]