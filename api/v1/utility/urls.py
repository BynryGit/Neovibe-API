__author__ = "aki"

from django.urls import path

from v1.utility.views.utility import UtilityListDetail, UtilityDetail
from v1.utility.views.summary import UtilityUsageSummaryDetail
from v1.utility.views.utility_module import UtilityModules, UtilityModuleDetail
from v1.utility.views.utility_sub_module import UtilitySubModules, UtilitySubModuleDetail

urlpatterns = [
    path('', UtilityListDetail.as_view(), name='utility_list'),
    path('<uuid:id_string>', UtilityDetail.as_view(),name='utility_detail'),
    path('<uuid:id_string>/summary', UtilityUsageSummaryDetail.as_view(), name='utility_summary'),
    path('<uuid:id_string>/module', UtilityModules.as_view(), name='utility_module_list'),
    path('<uuid:utility>/module/<uuid:module>', UtilityModuleDetail.as_view(), name='utility_module_details'),
    path('<uuid:utility>/module/<uuid:module>/submodule', UtilitySubModules.as_view(), name='utility_submodule_list'),
    path('<uuid:utility>/module/<uuid:module>/submodule/<uuid:submodule>', UtilitySubModuleDetail.as_view(), name='utility_submodule_details'),
]