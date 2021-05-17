from django.urls import path
from v1.commonapp.views.city import CityList, City, CityDetail
from v1.commonapp.views.country import CountryList, Country, CountryDetail
from v1.commonapp.views.currency import CurrencyList
from v1.commonapp.views.department import Department, DepartmentListByTenant, DepartmentListByUtility, \
    DepartmentTypeDetail, DepartmentTypeList, DepartmentType
from v1.commonapp.views.department_subtype import DepartmentSubType, DepartmentSubTypeDetail, DepartmentSubTypeList
from v1.commonapp.views.global_lookup import Global_LookupList
from v1.commonapp.views.region import RegionList, Region, RegionDetail
from v1.commonapp.views.state import StateList, State, StateDetail
from v1.commonapp.views.zone import ZoneList, Zone, ZoneDetail
from v1.commonapp.views.division import DivisionList, Division, DivisionDetail
from v1.commonapp.views.area import AreaList, AreaDetail, Area
from v1.commonapp.views.form_factor import FormFactor, FormFactorList
from v1.commonapp.views.sub_area import SubAreaList, SubAreaDetail, SubArea, SubAreaListByArea
from v1.commonapp.views.module import ModuleList
from v1.commonapp.views.sub_modules import SubModule, SubModuleList
from v1.commonapp.views.frequency import FrequencyList, FrequencyDetail
from v1.commonapp.views.products import ProductList, ProductDetail, Product
# from v1.userapp.views.role_sub_type import RoleSubType, RoleSubTypeList
from v1.userapp.views.role_type import RoleTypeList
from v1.userapp.views.user_type import UserTypeList
from v1.commonapp.views.skills import SkillsList, SkillDetail, Skill
from v1.userapp.views.role_sub_type import RoleSubTypeByRoleType
from v1.commonapp.views.premises import PremiseList, Premise, PremiseList, PremiseShortList, PremiseDetail
from v1.commonapp.views.channel import ChannelList, Channel
from v1.commonapp.views.frequency import FrequencyDetail, FrequencyList, Frequency
from v1.commonapp.views.document_type import DocumentTypeList, DocumentTypeDetail, DocumentType
from v1.commonapp.views.document_subtype import DocumentSubTypeList, DocumentSubTypeDetail, DocumentSubType
from v1.commonapp.views.document import Document, DocumentList, DocumentDetail, GlobalDocumentList
from v1.commonapp.views.notification_type import NotificationTypeList, NotificationTypeDetail, NotificationType
from v1.commonapp.views.notification_subtype import NotificationSubTypeList, NotificationSubTypeDetail, \
    NotificationSubType
from v1.commonapp.views.integration_type import IntegrationTypeList
from v1.commonapp.views.work_order_type import WorkOrderTypeList,WorkOrderType,WorkOrderTypeDetail
from v1.commonapp.views.work_order_sub_type import WorkOrderSubTypeList,WorkOrderSubType,WorkOrderSubTypeDetail
from v1.commonapp.views.integration_subtype import IntegrationSubTypeList
from v1.commonapp.views.integration_master import IntegrationMasterList, IntegrationMasterDetail, IntegrationMaster
from v1.commonapp.views.document import UploadDocument
from v1.commonapp.views.meter_status import MeterStatusList
from v1.commonapp.views.admin_life_cycle import AdminLifeCycleList
from v1.commonapp.views.notification_template import NotificationTemplateList, NotificationTemplate, NotificationTemplateDetail
urlpatterns = [
    path('document/list', GlobalDocumentList.as_view()),
    path('utility/region', Region.as_view()),
    path('utility/work-order-type', WorkOrderType.as_view()),
    path('utility/work-order-type/<uuid:id_string>', WorkOrderTypeDetail.as_view()),
    path('utility/work-order-sub-type', WorkOrderSubType.as_view()),
    path('utility/work-order-sub-type/<uuid:id_string>', WorkOrderSubTypeDetail.as_view()),
    path('utility/document_type/<uuid:id_string>', DocumentTypeDetail.as_view()),
    path('utility/document_type', DocumentType.as_view()),
    path('utility/document_subtype/<uuid:id_string>', DocumentSubTypeDetail.as_view()),
    path('utility/document_subtype', DocumentSubType.as_view()),
    path('utility/document/<uuid:id_string>', DocumentDetail.as_view()),
    path('utility/document', Document.as_view()),
    path('utility/region/<uuid:id_string>', RegionDetail.as_view()),
    path('utility/country', Country.as_view()),
    path('utility/country/<uuid:id_string>', CountryDetail.as_view()),
    path('utility/state', State.as_view()),
    path('utility/state/<uuid:id_string>', StateDetail.as_view()),
    path('utility/city', City.as_view()),
    path('utility/city/<uuid:id_string>', CityDetail.as_view()),
    path('utility/zone', Zone.as_view()),
    path('utility/division/<uuid:id_string>', DivisionDetail.as_view()),
    path('utility/division', Division.as_view()),
    path('utility/zone/<uuid:id_string>', ZoneDetail.as_view()),
    path('utility/area', Area.as_view()),
    path('utility/area/<uuid:id_string>', AreaDetail.as_view()),
    path('utility/subarea', SubArea.as_view()),
    path('utility/subarea/<uuid:id_string>', SubAreaDetail.as_view()),
    path('utility/premise', Premise.as_view()),
    path('utility/<uuid:id_string>/premise/short_list', PremiseShortList.as_view()),
    path('utility/premise/<uuid:id_string>', PremiseDetail.as_view()),
    path('utility/skill/<uuid:id_string>', SkillDetail.as_view()),
    path('utility/skill', Skill.as_view()),
    path('sub_area/list', SubAreaList.as_view()),
    path('utility/<uuid:id_string>/frequency/list', FrequencyList.as_view()),
    path('utility/frequency/<uuid:id_string>', FrequencyDetail.as_view()),
    path('utility/frequency', Frequency.as_view()),
    path('product/list', ProductList.as_view()),
    path('utility/product', Product.as_view()),
    path('utility/product/<uuid:id_string>', ProductDetail.as_view()),
    path('dept-type/list', DepartmentTypeList.as_view()),
    path('utility/dept-type', DepartmentType.as_view()),
    path('utility/dept-type/<uuid:id_string>', DepartmentTypeDetail.as_view()),
    path('utility/notification_type', NotificationType.as_view()),
    path('utility/notification_type/<uuid:id_string>', NotificationTypeDetail.as_view()),
    path('utility/notification_subtype', NotificationSubType.as_view()),
    path('utility/notification_subtype/<uuid:id_string>', NotificationSubTypeDetail.as_view()),
    path('dept_subtype/list', DepartmentSubTypeList.as_view()),
    path('integration-type/list', IntegrationTypeList.as_view()),
    path('integration-subtype/list', IntegrationSubTypeList.as_view()),
    path('utility/<uuid:id_string>/integration-master/list', IntegrationMasterList.as_view()),
    path('utility/integration-master/<uuid:id_string>', IntegrationMasterDetail.as_view()),
    path('utility/integration-master', IntegrationMaster.as_view()),
    path('utility/dept_subtype', DepartmentSubType.as_view()),
    path('utility/dept_subtype/<uuid:id_string>', DepartmentSubTypeDetail.as_view()),
    # path('role_type/<uuid:id_string>', RoleType.as_view()),
    # path('role_type/list', RoleTypeList.as_view()),
    # path('role_subtype/<uuid:id_string>', RoleSubType.as_view()),
    # path('role_subtype/list', RoleSubTypeList.as_view()),
    path('form_factors', FormFactor.as_view()),
    path('form-factor/list', FormFactorList.as_view()),
    path('department/<uuid:id_string>', Department.as_view()),
    path('<uuid:id_string>/department/list', DepartmentListByTenant.as_view()),
    path('<uuid:id_string>/departments/list', DepartmentListByUtility.as_view()),
    path('module/list', ModuleList.as_view()),
    path('submodule/<uuid:id_string>', SubModule.as_view()),
    path('submodule/list', SubModuleList.as_view()),
    # This api used for utility dropdown start
    path('region/list', RegionList.as_view(), name='regions_list'),
    path('work-order-type/list', WorkOrderTypeList.as_view(), name='work_order_type_list'),
    path('work-order-sub-type/list', WorkOrderSubTypeList.as_view(), name='work_order_sub_type_list'),
    path('document_type/list', DocumentTypeList.as_view(), name='document_type_list'),
    path('channel/list', ChannelList.as_view(), name='channel_list'),
    path('utility/channel', Channel.as_view(), name='channel_add'),
    path('utility/<uuid:id_string>/country/list', CountryList.as_view(), name='country_list'),
    path('utility/<uuid:id_string>/state/list', StateList.as_view(), name='state_list'),
    path('utility/<uuid:id_string>/document/list', DocumentList.as_view(), name='document_list'),
    path('utility/<uuid:id_string>/document_subtype/list', DocumentSubTypeList.as_view(), name='document_subtype_list'),
    path('utility/<uuid:id_string>/city/list', CityList.as_view(), name='city_list'),
    path('utility/<uuid:id_string>/zone/list', ZoneList.as_view(), name='zone_list'),
    path('utility/<uuid:id_string>/division/list', DivisionList.as_view(), name='zone_list'),
    path('utility/<uuid:id_string>/area/list', AreaList.as_view(), name='area_list'),
    path('utility/<uuid:id_string>/subarea/list', SubAreaList.as_view(), name='subarea_list'),
    path('utility/<uuid:id_string>/premise/list', PremiseList.as_view(), name='premise_list'),
    path('utility/<uuid:id_string>/notification_type/list', NotificationTypeList.as_view(),
         name='notification_type_list'),
    path('utility/<uuid:id_string>/notification_subtype/list', NotificationSubTypeList.as_view(),
         name='notification_subtype_list'),
    # This api used for utility dropdown end
    path('<uuid:id_string>/areas', AreaList.as_view()),
    path('<uuid:id_string>/sub-areas', SubAreaList.as_view()),
    path('area/<uuid:id_string>/sub-areas', SubAreaListByArea.as_view()),
    path('sub-area/<uuid:id_string>/premises', PremiseList.as_view()),
    # path('<uuid:id_string>/cities', CityList.as_view()),
    path('<uuid:id_string>/states', StateList.as_view()),
    path('role-type/<uuid:id_string>/list', RoleTypeList.as_view()),
    path('utility/<uuid:id_string>/skill/list', SkillsList.as_view()),
    path('user-type/list', UserTypeList.as_view()),
    path('<uuid:id_string>/skill/list', SkillsList.as_view()),
    path('role-type/<uuid:id_string>/role-subtype/list', RoleSubTypeByRoleType.as_view(), name='utility_status_list'),
    path('<uuid:id_string>/state/list', StateList.as_view(), name='state_list'),
    path('currency/list', CurrencyList.as_view()),
    path('global-lookup/list', Global_LookupList.as_view()),
    path('document/upload',UploadDocument.as_view(), name="upload_document"),
    path('meter-status/list',MeterStatusList.as_view(), name="meter_status_list"),
    path('utility/<uuid:id_string>/notification-template/list', NotificationTemplateList.as_view(), name="notification_template_list"),
    path('utility/notification-template', NotificationTemplate.as_view(), name="notification_template"),
    path('utility/notification-template/<uuid:id_string>', NotificationTemplateDetail.as_view(), name="notification_template_detail"),
    path('admin/<uuid:id_string>/life-cycle/list',AdminLifeCycleList.as_view(), name="admin-life-cycle-list")

]
