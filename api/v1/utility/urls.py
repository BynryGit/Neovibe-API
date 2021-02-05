__author__ = "aki"

from django.urls import path
from v1.utility.views.document import UtilityDocumentList, UtilityDocumentDetail
from v1.utility.views.document_sub_type import UtilityDocumentSubTypeList
from v1.utility.views.notes import UtilityNoteList, UtilityNoteDetail
from v1.utility.views.status import UtilityStatusList
from v1.utility.views.utility import UtilityList, UtilityDetail, Utility, UtilityModule
from v1.utility.views.summary import UtilitySummaryDetail
from v1.utility.views.utility_currency import UtilityCurrencyList
from v1.utility.views.utility_module import UtilityModuleList, UtilityModuleDetail
from v1.utility.views.utility_module_submodule import UtilityModuleSubmoduleList
from v1.utility.views.utility_service import UtilityServiceList
from v1.utility.views.utility_service_contract_master import UtilityServiceContractMasterList, \
    UtilityServiceContractMasterDetail, UtilityServiceContractMaster
from v1.utility.views.utility_service_request_sub_type import UtilityServiceRequestSubTypeList
from v1.utility.views.utility_service_request_type import UtilityServiceRequestTypeList
from v1.utility.views.utility_sub_module import UtilitySubModuleList, UtilitySubModuleDetail, \
    UtilitySubModuleListByModule,UtilitySubModuleListByUtility, api_delete_submodule
from v1.userapp.views.role_type import RoleTypeList,RoleTypeListByUtility
from v1.utility.views.utility_region import UtilityRegionList
from v1.utility.views.numformat import UtilityNumFormatList,UtilityNumformatDetail, UtilityNumFormat
from v1.utility.views.utility_payment_channel import UtilityPaymentChannelList
# from v1.userapp.views.role_type import RoleTypeListByUtility
from v1.userapp.views.role_sub_type import RoleSubTypeByRoleType
from v1.utility.views.utility_payment_type import UtilityPaymentTypeList
from v1.utility.views.utility_payment_subtype import UtilityPaymentSubTypeList
from v1.utility.views.utility_payment_mode import UtilityPaymentModeList
from v1.utility.views.utility_leave_type import UtilityLeaveTypeList
from v1.utility.views.utility_product import UtilityProductList
from v1.userapp.views.role_type import RoleTypeList, RoleTypeListByUtility
from v1.utility.views.utility_department_type import UtilityDepartmentTypeList
from v1.utility.views.utility_department_subtype import UtilityDepartmentSubTypeList
from v1.utility.views.utility_document_type import UtilityDocumentTypeList
from v1.userapp.views.role_type import RoleTypeListByUtility
from v1.userapp.views.role_sub_type import RoleSubTypeByRoleType, RoleSubTypeListByUtility
from v1.utility.views.utility_region import UtilityRegionList
from v1.utility.views.utility_holiday_calendar import HolidayList, Holiday, HolidayDetail
from v1.utility.views.utility_working_hours import WorkingHourList, WorkingHour, WorkingHourDetail
from v1.utility.views.utility_service_contract_template import UtilityServiceContractTemplateList
# from v1.utility.views.utility_country import UtilityCountryList
# from v1.utility.views.utility_state import UtilityStateList

urlpatterns = [
    path('', Utility.as_view(), name='utility'),
    path('list', UtilityList.as_view(), name='utility_list'),
    path('<uuid:id_string>', UtilityDetail.as_view(), name='utility_detail'),
    path('module', UtilityModule.as_view(), name='utility_detail'),
    path('<uuid:id_string>/summary', UtilitySummaryDetail.as_view(), name='utility_summary'),

    path('<uuid:id_string>/module/list', UtilityModuleList.as_view(), name='utility_module_list'),
    path('module/<uuid:id_string>', UtilityModuleDetail.as_view(), name='utility_module_details'),
    path('submodule/<uuid:id_string>', UtilitySubModuleDetail.as_view(), name='utility_submodule_details'),
    path('module/<uuid:id_string>/submodule/list', UtilitySubModuleListByModule.as_view(),
         name='utility_submodule_list_by_module'),

    path('<uuid:id_string>/module-submodule/list', UtilityModuleSubmoduleList.as_view(), name='utility_module_list'),

    path('<uuid:id_string>/documents', UtilityDocumentList.as_view(), name='utility_document_list'),
    path('document/<uuid:id_string>', UtilityDocumentDetail.as_view(), name='utility_document_details'),

    path('<uuid:id_string>/notes', UtilityNoteList.as_view(), name='utility_notes_list'),
    path('note/<uuid:id_string>', UtilityNoteDetail.as_view(), name='utility_note_details'),
    path('<uuid:id_string>/status/list', UtilityStatusList.as_view(),name='utility_status_list'),

    path('<uuid:id_string>/numformat', UtilityNumformatDetail.as_view(), name='numformat'),

    path('<uuid:id_string>/status/list', UtilityStatusList.as_view(), name='utility_status_list'),
    path('<uuid:id_string>/document-type/list', UtilityDocumentTypeList.as_view(), name='utility_document_type_list'),
    path('<uuid:id_string>/role-type/list', RoleTypeListByUtility.as_view()),
    path('<uuid:id_string>/role-subtype/list', RoleSubTypeListByUtility.as_view()),
    path('<uuid:id_string>/dept-type/list', UtilityDepartmentTypeList.as_view()),
    path('<uuid:id_string>/dept-subtype/list', UtilityDepartmentSubTypeList.as_view()),
    path('<uuid:id_string>/currency/list', UtilityCurrencyList.as_view()),
    path('role-type/<uuid:id_string>/role-subtype/list', RoleSubTypeByRoleType.as_view(),name='utility_status_list'),
    path('<uuid:id_string>/region/list', UtilityRegionList.as_view(), name='utility_region_list'),
    path('<uuid:id_string>/product/list', UtilityProductList.as_view(), name='utility_product_list'),
    path('<uuid:id_string>/payment/channel/list', UtilityPaymentChannelList.as_view(), name='utility_payment_channel_list'),
    path('<uuid:id_string>/payment/type/list', UtilityPaymentTypeList.as_view(), name='utility_payment_type_list'),
    path('<uuid:id_string>/payment/subtype/list', UtilityPaymentSubTypeList.as_view(), name='utility_payment_subtype_list'),
    path('<uuid:id_string>/payment/mode/list', UtilityPaymentModeList.as_view(), name='utility_payment_mode_list'),
    path('<uuid:id_string>/numformat/list', UtilityNumFormatList.as_view(), name='utility_num_format_list'),
    path('<uuid:id_string>/numformat', UtilityNumformatDetail.as_view(), name='numformat'),
    path('numformat', UtilityNumFormat.as_view(), name='numformat'),
    path('<uuid:id_string>/sub_module/list', UtilitySubModuleListByUtility.as_view()),
    path('<uuid:id_string>/sub_module/delete',api_delete_submodule, name="delete"),
    path('role-type/<uuid:id_string>/role-subtype/list', RoleSubTypeByRoleType.as_view(), name='role_subtype_list'),
    path('<uuid:id_string>/region/list', UtilityRegionList.as_view()),
    path('<uuid:id_string>/holiday/list', HolidayList.as_view()),
    path('holiday', Holiday.as_view()),
    path('holiday/<uuid:id_string>', HolidayDetail.as_view()),
    path('<uuid:id_string>/working_hour/list', WorkingHourList.as_view()),
    path('working_hour', WorkingHour.as_view()),
    path('working_hour/<uuid:id_string>', WorkingHourDetail.as_view()),
    path('<uuid:id_string>/leave_type/list', UtilityLeaveTypeList.as_view()),
    path('<uuid:id_string>/service/list', UtilityServiceList.as_view(), name='utility_service_list'),
    path('<uuid:id_string>/service-contract-template/list', UtilityServiceContractTemplateList.as_view()),
    path('<uuid:id_string>/service-contract/list', UtilityServiceContractMasterList.as_view(),
         name='utility_service_contract_master_list'),
    path('service-contract', UtilityServiceContractMaster.as_view(),
         name='utility_service_contract_master_post'),
    path('service-contract/<uuid:id_string>', UtilityServiceContractMasterDetail.as_view()),
    path('<uuid:id_string>/service-request-type/list', UtilityServiceRequestTypeList.as_view()),
    path('<uuid:id_string>/service-request-sub-type/list', UtilityServiceRequestSubTypeList.as_view()),

]
